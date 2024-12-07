# coding: utf-8

"""
module to define a standard tomography acquisition (made by bliss)
"""
from __future__ import annotations

from datetime import datetime

import h5py
from silx.io.url import DataUrl
from silx.io.utils import h5py_read_dataset
from pyunitsystem import ElectricCurrentSystem, MetricSystem

from nxtomo.utils.transformation import DetYFlipTransformation, DetZFlipTransformation
from nxtomo.nxobject.nxsource import SourceType
from nxtomo.nxobject.nxdetector import ImageKey

from nxtomomill.io.acquisitionstep import AcquisitionStep
from nxtomomill.utils.utils import str_datetime_to_numpy_datetime64

from .baseacquisition import BaseAcquisition, EntryReader
from .utils import (
    deduce_machine_current,
    get_entry_type,
    get_nx_detectors,
    guess_nx_detector,
)

try:
    import hdf5plugin  # noqa F401
except ImportError:
    pass
import fnmatch
import logging
import os

import numpy

from nxtomomill.converter.hdf5.acquisition.blisstomoconfig import (
    TomoConfig as BlissTomoConfig,
)
from nxtomomill.io.config import TomoHDF5Config
from nxtomo.application.nxtomo import NXtomo

_logger = logging.getLogger(__name__)


__all__ = [
    "StandardAcquisition",
]


class StandardAcquisition(BaseAcquisition):
    """
    Class to collect information from a bliss - hdf scan (see https://bliss.gitlab-pages.esrf.fr/fscan).
    Once all data is collected a set of NXtomo will be created.
    Then NXtomo instances will be saved to disk.

    :param root_url: url of the acquisition. Can be None if
                             this is the initialization entry
    :param configuration: configuration to use to collect raw data and generate outputs
    :param detector_sel_callback: possible callback to retrieve missing information
    """

    def __init__(
        self,
        root_url: DataUrl | None,
        configuration: TomoHDF5Config,
        detector_sel_callback,
        start_index,
        parent=None,
    ):
        super().__init__(
            root_url=root_url,
            configuration=configuration,
            detector_sel_callback=detector_sel_callback,
            start_index=start_index,
        )
        self._parent = parent
        # possible parent. Like for z series
        self._nx_tomos = [NXtomo()]
        self._image_key_control = None
        self._rotation_angle = None
        self._sample_x = None
        self._sample_y = None
        self._translation_y = None
        self._translation_z = None
        self._x_flipped = None
        self._y_flipped = None

        self._unique_detector_names = list()
        # register names

        self._virtual_sources = None
        self._acq_expo_time = None
        self._copied_dataset = {}
        "register dataset copied. Key if the original location as" "DataUrl.path. Value is the DataUrl it has been moved to"
        self._known_machine_electric_current = None
        # store all registred amchine electric current
        self._frames_timestamp = None
        # try to deduce time stamp of each frame

    def parent_root_url(self) -> DataUrl | None:
        if self._parent is not None:
            return self._parent.root_url
        else:
            return None

    def get_expected_nx_tomo(self):
        return 1

    @property
    def image_key_control(self):
        return self._image_key_control

    @property
    def rotation_angle(self):
        return self._rotation_angle

    @property
    def translation_y(self):
        return self._translation_y

    @property
    def translation_z(self):
        return self._translation_z

    @property
    def x_flipped(self):
        return self._x_flipped

    @property
    def y_flipped(self):
        return self._y_flipped

    @property
    def n_frames(self):
        return self._n_frames

    @property
    def n_frames_actual_bliss_scan(self):
        return self._n_frames_actual_bliss_scan

    @property
    def dim_1(self):
        return self._dim_1

    @property
    def dim_2(self):
        return self._dim_2

    @property
    def data_type(self):
        return self._data_type

    @property
    def expo_time(self):
        return self._acq_expo_time

    @property
    def known_machine_electric_current(self) -> dict | None:
        """
        Return the dict of all know machine electric current. Key is the time stamp, value is the electric current
        """
        return self._known_machine_electric_current

    @property
    def sample_x(self):
        """Return the '_sample_x' attribute."""
        return self._sample_x

    @property
    def sample_y(self):
        """Return the '_sample_y' attribute."""
        return self._sample_y

    def register_step(
        self,
        url: DataUrl,
        entry_type: AcquisitionStep | None = None,
        copy_frames=False,
    ) -> None:
        """

        :param url: entry to be registered and contained in the
                                 acquisition
        :param entry_type: type of the entry if know. Overwise will be
                           'evaluated'
        """
        if entry_type is None:
            entry_type = get_entry_type(url=url, configuration=self.configuration)
        assert (
            entry_type is not AcquisitionStep.INITIALIZATION
        ), "Initialization are root node of a new sequence and not a scan of a sequence"

        if entry_type is None:
            _logger.warning(f"{url} not recognized, skip it")
        else:
            self._registered_entries[url.path()] = entry_type
            self._copy_frames[url.path()] = copy_frames
            self._entries_o_path[url.path()] = url.data_path()
            # path from the original file. Haven't found another way to get it ?!

    def _get_valid_camera_names(self, instrument_grp: h5py.Group):
        # 1: try to get detector from nx property
        detectors = get_nx_detectors(instrument_grp)
        detectors = [grp.name.split("/")[-1] for grp in detectors]

        def filter_detectors(det_grps):
            if len(det_grps) > 0:
                _logger.info(f"{len(det_grps)} detector found from NX_class attribute")
                if len(det_grps) > 1:
                    # if an option: pick the first one once orderered
                    # else ask user
                    if self._detector_sel_callback is None:
                        sel_det = det_grps[0]
                        _logger.warning(
                            f"several detector found. Only one is managed for now. Will pick {sel_det}"
                        )
                    else:
                        sel_det = self._detector_sel_callback(det_grps)
                        if sel_det is None:
                            _logger.warning("no detector given, avoid conversion")
                    det_grps = (sel_det,)
                return det_grps
            return None

        detectors = filter_detectors(det_grps=detectors)
        if detectors is not None:
            return detectors

        # 2: get nx detector from shape...
        detectors = guess_nx_detector(instrument_grp)
        detectors = [grp.name.split("/")[-1] for grp in detectors]
        return filter_detectors(det_grps=detectors)

    def __get_data_from_camera(
        self,
        data_dataset: h5py.Dataset,
        data_name,
        frame_type,
        entry,
        entry_path,
        camera_dataset_url,
    ):
        if data_dataset.ndim == 2:
            shape = (1, data_dataset.shape[0], data_dataset.shape[1])
        elif data_dataset.ndim != 3:
            err = f"dataset {data_name} is expected to be 3D when {data_dataset.ndim}D found."
            if data_dataset.ndim == 1:
                err = "\n".join(
                    [
                        err,
                        "This might be a bliss-EDF dataset. Those are not handled by nxtomomill",
                    ]
                )
            _logger.error(err)
            return 0
        else:
            shape = data_dataset.shape

        n_frame = shape[0]
        self._n_frames += n_frame
        self._n_frames_actual_bliss_scan = n_frame
        if self.dim_1 is None:
            self._dim_2 = shape[1]
            self._dim_1 = shape[2]
        else:
            if self._dim_1 != shape[2] or self._dim_2 != shape[1]:
                raise ValueError("Inconsistency in detector shapes")
        if self._data_type is None:
            self._data_type = data_dataset.dtype
        elif self._data_type != data_dataset.dtype:
            raise ValueError("detector frames have incoherent " "data types")

        # update image_key and image_key_control
        # Note: for now there is no image_key on the master file
        # should be added later.
        image_key_control = frame_type.to_image_key_control()
        self._image_key_control.extend([image_key_control.value] * n_frame)

        data_dataset_path = data_dataset.name.replace(entry.name, entry_path, 1)
        # replace data_dataset name by the original entry_path.
        # this is a workaround to use the dataset path on the
        # "treated file". Because .name if the name on the 'target'
        # file of the virtual dataset
        v_source = h5py.VirtualSource(
            camera_dataset_url.file_path(),
            data_dataset_path,
            data_dataset.shape,
            dtype=self._data_type,
        )
        self._virtual_sources.append(v_source)
        self._virtual_sources_len.append(n_frame)
        return n_frame

    def _treate_valid_camera(
        self,
        detector_node,
        entry,
        frame_type,
        input_file_path,
        entry_path,
        entry_url,
    ) -> bool:
        """
        return True if the entry contains frames
        """
        if "data_cast" in detector_node:
            _logger.warning(
                f"!!! looks like this data has been cast. Take cast data for {detector_node}!!!"
            )
            data_dataset = detector_node["data_cast"]
            data_name = "/".join((detector_node.name, "data_cast"))
        else:
            data_dataset = detector_node["data"]
            data_name = "/".join((detector_node.name, "data"))

        camera_dataset_url = DataUrl(
            file_path=entry_url.file_path(), data_path=data_name, scheme="silx"
        )

        n_frame = self.__get_data_from_camera(
            data_dataset,
            data_name=data_name,
            frame_type=frame_type,
            entry=entry,
            entry_path=entry_path,
            camera_dataset_url=camera_dataset_url,
        )
        # save information if this url must be embed / copy or not. Will be used later at nxtomo side
        self._copy_frames[camera_dataset_url.path()] = self._copy_frames[
            entry_url.path()
        ]

        x_flipped, y_flipped = self._get_flipped_frame()
        if x_flipped is not None and y_flipped is not None:
            if self._x_flipped is None and self._y_flipped is None:
                self._x_flipped, self._y_flipped = bool(x_flipped), bool(y_flipped)
            elif x_flipped != self._x_flipped or y_flipped != self._y_flipped:
                raise ValueError(
                    f"Found different detector flips inside the same sequence on {entry}. Unable to handle it."
                )
        # store rotation
        rots = self._get_rotation_angle(root_node=entry, n_frame=n_frame)[0]
        self._rotation_angle.extend(rots)

        self._sample_x.extend(self._get_sample_x(root_node=entry, n_frame=n_frame)[0])

        self._sample_y.extend(self._get_sample_y(root_node=entry, n_frame=n_frame)[0])

        self._translation_y.extend(
            self._get_translation_y(root_node=entry, n_frame=n_frame)[0]
        )

        self._translation_z.extend(
            self._get_translation_z(root_node=entry, n_frame=n_frame)[0]
        )

        # store acquisition time
        self._acq_expo_time.extend(
            self._get_expo_time(
                root_node=entry,
                detector_node=detector_node,
                n_frame=n_frame,
            )[0]
        )

        self._current_scan_n_frame = n_frame

    def camera_is_valid(self, det_name):
        assert isinstance(det_name, str)
        if self.configuration.valid_camera_names is None:
            return True
        for vcm in self.configuration.valid_camera_names:
            if fnmatch.fnmatch(det_name, vcm):
                return True
        return False

    def _preprocess_registered_entry(self, entry_url, type_):
        with EntryReader(entry_url) as entry:
            entry_path = self._entries_o_path[entry_url.path()]
            input_file_path = entry_url.file_path()
            input_file_path = os.path.abspath(
                os.path.relpath(input_file_path, os.getcwd())
            )
            input_file_path = os.path.abspath(input_file_path)
            if type_ is AcquisitionStep.INITIALIZATION:
                raise RuntimeError(
                    "no initialization should be registered."
                    "There should be only one per acquisition."
                )

            if "instrument" not in entry:
                _logger.error(
                    f"no instrument group found in {entry.name}, unable to retrieve frames"
                )
                return

            instrument_grp = entry["instrument"]

            # if we don't get a valid camera (not provided by the user or not found on the bliss tomo metadata)
            if self.configuration.valid_camera_names is None:
                # if we need to guess detector name(s)
                # ignore in case we read information from bliss config
                det_grps = self._get_valid_camera_names(instrument_grp)
                # update valid camera names
                self.configuration.valid_camera_names = det_grps
            has_frames = False
            for key, _ in instrument_grp.items():
                if (
                    "NX_class" in instrument_grp[key].attrs
                    and instrument_grp[key].attrs["NX_class"] == "NXdetector"
                ):
                    _logger.debug(f"Found one detector at {key} for {entry.name}.")

                    if not self.camera_is_valid(key):
                        _logger.debug(f"ignore {key}, not a `valid` camera name")
                        continue
                    else:
                        detector_node = instrument_grp[key]
                        if key not in self._unique_detector_names:
                            self._unique_detector_names.append(key)
                        self._treate_valid_camera(
                            detector_node,
                            entry=entry,
                            frame_type=type_,
                            input_file_path=input_file_path,
                            entry_path=entry_path,
                            entry_url=entry_url,
                        )
                        has_frames = True
            # try to get some other metadata

            # handle frame time stamp
            start_time = self._get_start_time(entry)
            if start_time is not None:
                start_time = datetime.fromisoformat(start_time)
            end_time = self._get_end_time(entry)
            if end_time is not None:
                end_time = datetime.fromisoformat(end_time)
            if has_frames:
                self._register_frame_timestamp(entry, start_time, end_time)

            # handle electric current. Can retrieve some current even on bliss scan entry doesn;t containing directly frames
            self._register_machine_electric_current(entry, start_time, end_time)

    def _register_machine_electric_current(
        self, entry: h5py.Group, start_time, end_time
    ):
        """Update machine electric current for provided entry (bliss scan"""
        (
            electric_currents,
            electric_current_unit,
        ) = self._get_electric_current(root_node=entry)
        electric_current_unit_ref = ElectricCurrentSystem.AMPERE
        # electric current will be saved as Ampere
        if electric_currents is not None and len(electric_currents) > 0:
            if electric_current_unit is None:
                electric_current_unit = ElectricCurrentSystem.MILLIAMPERE
                _logger.warning(
                    "No unit found for electric current. Consider it as mA."
                )

            unit_factor = (
                ElectricCurrentSystem.from_str(electric_current_unit).value
                / electric_current_unit_ref.value
            )

            new_know_electric_currents = {}
            if start_time is None or end_time is None:
                if start_time != end_time:
                    _logger.warning(
                        f"Unable to find {'start_time' if start_time is None else 'end_time'}. Will pick the first available electric_current for the frame"
                    )
                    t_time = start_time or end_time
                    # if at least one can find out
                    new_know_electric_currents[
                        str_datetime_to_numpy_datetime64(t_time)
                    ] = (electric_currents[0] * unit_factor)
                else:
                    _logger.error(
                        "Unable to find start_time and end_time. Will not register any machine electric current"
                    )
            elif len(electric_currents) == 1:
                # if we have only one value, consider the machine electric current is constant during this time
                # might be improved later if we can know if current is determine at the
                # beginning or the end. But should have no impact
                # as the time slot is short
                new_know_electric_currents[
                    str_datetime_to_numpy_datetime64(start_time)
                ] = (electric_currents[0] * unit_factor)
            else:
                # linspace from datetime within ms precision.
                # see https://localcoder.org/creating-numpy-linspace-out-of-datetime#credit_4
                # and https://stackoverflow.com/questions/37964100/creating-numpy-linspace-out-of-datetime
                timestamps = numpy.linspace(
                    start=str_datetime_to_numpy_datetime64(start_time).astype(
                        numpy.float128
                    ),
                    stop=str_datetime_to_numpy_datetime64(end_time).astype(
                        numpy.float128
                    ),
                    num=len(electric_currents),
                    endpoint=True,
                    dtype="<M8[ms]",
                )
                for timestamp, mach_electric_current in zip(
                    timestamps, electric_currents
                ):
                    new_know_electric_currents[timestamp.astype(numpy.datetime64)] = (
                        mach_electric_current * unit_factor
                    )
            self._known_machine_electric_current.update(new_know_electric_currents)

    def _register_frame_timestamp(self, entry: h5py.Group, start_time, end_time):
        """
        update frame time stamp for the provided entry (bliss scan)
        """
        if start_time is None or end_time is None:
            if start_time != end_time:
                t_time = str_datetime_to_numpy_datetime64(start_time or end_time)
                message = f"Unable to find start_time and / or end_time. Takes {t_time} as frame time stamp for {entry} "
                self._frames_timestamp.extend(
                    [t_time] * self._n_frames_actual_bliss_scan
                )
                _logger.warning(message)
            else:
                message = f"Unable to find start_time and end_time. Can't deduce frames time stamp for {entry}"
                _logger.error(message)
        else:
            frames_times_stamps_as_f8 = numpy.linspace(
                start=str_datetime_to_numpy_datetime64(start_time).astype(
                    numpy.float128
                ),
                stop=str_datetime_to_numpy_datetime64(end_time).astype(numpy.float128),
                num=self._n_frames_actual_bliss_scan,
                endpoint=True,
                dtype="<M8[ms]",
            )
            frames_times_stamps_as_f8 = [
                timestamp.astype("<M8[ms]") for timestamp in frames_times_stamps_as_f8
            ]
            self._frames_timestamp.extend(frames_times_stamps_as_f8)

    def _preprocess_registered_entries(self):
        """parse all frames of the different steps and retrieve data,
        image_key..."""
        self._n_frames = 0
        self._n_frames_actual_bliss_scan = 0
        # number of frame contains in X.1
        self._dim_1 = None
        self._dim_2 = None
        self._data_type = None
        self._translation_y = []
        self._translation_z = []
        self._sample_x = []
        self._sample_y = []
        self._image_key_control = []
        self._rotation_angle = []
        self._known_machine_electric_current = {}
        self._frames_timestamp = []
        self._virtual_sources = []
        self._instrument_name = None
        self._virtual_sources_len = []
        self._diode = []
        self._acq_expo_time = []
        self._diode_unit = None
        self._copied_dataset = {}
        self._x_flipped = None
        self._y_flipped = None

        # if rotation motor is not defined try to deduce it from root_url/technique/scan/motor
        if self.configuration.rotation_angle_keys is None:
            rotation_motor = self._read_rotation_motor_name()
            if rotation_motor is not None:
                self.configuration.rotation_angle_keys = (rotation_motor,)
            else:
                self.configuration.rotation_angle_keys = tuple()

        # list of data virtual source for the virtual dataset
        for entry_url, type_ in self._registered_entries.items():
            url = DataUrl(path=entry_url)
            self._n_frames_actual_bliss_scan = 0
            self._preprocess_registered_entry(url, type_)

        if len(self._diode) == 0:
            self._diode = None
        if self._diode is not None:
            self._diode = numpy.asarray(self._diode)
            self._diode = self._diode / self._diode.mean()

    def _get_diode(self, root_node, n_frame) -> tuple:
        values, unit = self._get_node_values_for_frame_array(
            node=root_node["measurement"],
            n_frame=n_frame,
            keys=self.configuration.diode_keys,
            info_retrieve="diode",
            expected_unit="volt",
        )
        return values, unit

    def get_already_defined_params(self, key):
        defined = self.__get_extra_param(key=key)
        if len(defined) > 1:
            raise ValueError("{} are aliases. Only one should be defined")
        elif len(defined) == 0:
            return None
        else:
            return list(defined.values())[0]

    def __get_extra_param(self, key) -> dict:
        """return already defined parameters for one key.
        A key as aliases so it returns a dict"""
        aliases = list(TomoHDF5Config.EXTRA_PARAMS_ALIASES[key])
        aliases.append(key)
        res = {}
        for alias in aliases:
            if alias in self.configuration.param_already_defined:
                res[alias] = self.configuration.param_already_defined[alias]
        return res

    def _generic_path_getter(self, paths: tuple, message, level="warning", entry=None):
        """
        :param level: level can be logging.level values : "warning", "error", "info"
        :param H5group entry: user can provide directly an entry to be used as an open h5Group
        """
        if not isinstance(paths, tuple):
            raise TypeError

        url = self.parent_root_url() or self.root_url
        if url is not None:
            self._check_has_metadata(url)

        def process(h5_group):
            for path in paths:
                if h5_group is not None and path in h5_group:
                    return h5py_read_dataset(h5_group[path])
            if message is not None:
                getattr(_logger, level)(message)

        if entry is None:
            if url is None:
                return None
            with EntryReader(url) as h5_group:
                return process(h5_group)
        else:
            return process(entry)

    def _get_source_name(self):
        """ """
        return self._generic_path_getter(
            paths=self._SOURCE_NAME, message="Unable to find source name", level="info"
        )

    def _get_source_type(self):
        """ """
        return self._generic_path_getter(
            paths=self._SOURCE_TYPE, message="Unable to find source type", level="info"
        )

    def _get_title(self):
        """return acquisition title"""
        return self._generic_path_getter(
            paths=self._TITLE_PATH, message="Unable to find title"
        )

    def _get_instrument_name(self):
        """:return instrument instrument name (aka beamline name)"""
        name = self._generic_path_getter(
            paths=self._INSTRUMENT_NAME_PATH,
            message="Unable to find instrument name",
            level="info",
        )
        # on some path / old hdf5 the name is prefixed by "ESRF:". clean those
        if name is not None and name.startswith("ESRF:"):
            name = name.replace("ESRF:", "")
        return name

    def _get_dataset_name(self):
        """return name of the acquisition"""
        return self._generic_path_getter(
            paths=self._DATASET_NAME_PATH,
            message="No name describing the acquisition has been "
            "found, Name dataset will be skip",
        )

    def _get_sample_name(self):
        """return sample name"""
        return self._generic_path_getter(
            paths=self._SAMPLE_NAME_PATH,
            message="No sample name has been "
            "found, Sample name dataset will be skip",
        )

    def _get_grp_size(self):
        """return the nb_scans composing the zseries if is part of a group
        of sequence"""
        return self._generic_path_getter(
            paths=self._GRP_SIZE_PATH,
            message=None,
        )

    def _get_tomo_n(self):
        return self._generic_path_getter(
            paths=self._TOMO_N_PATH,
            message="unable to find information regarding tomo_n",
        )

    def _get_start_time(self, entry=None):
        return self._generic_path_getter(
            paths=self._START_TIME_PATH,
            message="Unable to find start time",
            level="info",
            entry=entry,
        )

    def _get_end_time(self, entry=None):
        return self._generic_path_getter(
            paths=self._END_TIME_PATH,
            message="Unable to find end time",
            level="info",
            entry=entry,
        )

    def _get_flipped_frame(self):
        url = self.parent_root_url() or self.root_url
        if url is None:
            return None, None
        self._check_has_metadata(url)
        with EntryReader(url) as entry:
            for flip_path in self._FRAME_FLIP_PATHS:
                if len(self._unique_detector_names) > 0:
                    key = flip_path.format(detector_name=self._unique_detector_names[0])
                else:
                    key = flip_path
                if key in entry:
                    return h5py_read_dataset(entry[key])
            else:
                return None, None

    def _get_energy(self, ask_if_0, input_callback):
        """return tuple(energy, unit)"""
        url = self.parent_root_url() or self.root_url
        if url is None:
            return None, None
        self._check_has_metadata()
        with EntryReader(url) as entry:
            if self._ENERGY_PATH in entry:
                energy = h5py_read_dataset(entry[self._ENERGY_PATH])
                unit = self._get_unit(entry[self._ENERGY_PATH], default_unit="kev")
                if energy == 0 and ask_if_0:
                    desc = (
                        "Energy has not been registered. Please enter "
                        "incoming beam energy (in kev):"
                    )
                    if input_callback is None:
                        en = input(desc)
                    else:
                        en = input_callback("energy", desc)
                    if energy is not None:
                        energy = float(en)
                return energy, unit
            else:
                mess = f"unable to find energy for entry {entry}."
                if self.raise_error_if_issue:
                    raise ValueError(mess)
                else:
                    mess += " Default value will be set (19kev)"
                    _logger.warning(mess)
                    return 19.0, "kev"

    def _get_sample_detector_distance(self):
        """return tuple(distance, unit)"""
        url = self.parent_root_url() or self.root_url
        if url is None:
            return None, None
        self._check_has_metadata(url)
        with EntryReader(url) as entry:
            for key in self.configuration.sample_detector_distance_paths:
                if key in entry:
                    node = entry[key]
                    distance = h5py_read_dataset(node)
                    unit = self._get_unit(node, default_unit="mm")
                    # convert to meter
                    distance = distance * MetricSystem.from_value(unit).value
                    return distance, "m"
            mess = f"unable to find distance for entry {entry}."
            if self.raise_error_if_issue:
                raise ValueError(mess)
            else:
                mess += "Default value will be set (1m)"
                _logger.warning(mess)
                return 1.0, "m"

    def _get_source_sample_distance(self):
        """return tuple(distance, unit)"""
        url = self.parent_root_url() or self.root_url
        if url is None:
            return None, None
        self._check_has_metadata(url)
        with EntryReader(url) as entry:
            for key in self.configuration.source_sample_distance_paths:
                if key in entry:
                    node = entry[key]
                    distance = h5py_read_dataset(node)
                    unit = self._get_unit(node, default_unit="mm")
                    # convert to meter
                    distance = distance * MetricSystem.from_value(unit).value
                    return distance, "m"
            mess = f"unable to find distance for entry {entry}."
            if self.raise_error_if_issue:
                raise ValueError(mess)
            else:
                mess += "Default value will be set (1m)"
                _logger.warning(mess)
                return 1.0, "m"

    def _get_pixel_size(self, axis):
        """return tuple(pixel_size, unit)"""
        url = self.parent_root_url() or self.root_url
        if url is None:
            return None, None
        if axis not in ("x", "y"):
            raise ValueError
        self._check_has_metadata()

        if axis == "x":
            keys = self.configuration.x_pixel_size_paths
        elif axis == "y":
            keys = self.configuration.y_pixel_size_paths
        else:
            raise ValueError(f"axis {axis} is invalid")

        with EntryReader(url) as entry:
            for key in keys:
                if key in entry:
                    node = entry[key]
                    node_item = h5py_read_dataset(node)
                    # if the pixel size is provided as x, y
                    if isinstance(node_item, numpy.ndarray):
                        if len(node_item) > 1 and axis == "y":
                            size_ = node_item[1]
                        else:
                            size_ = node_item[0]
                    # if this is a single value
                    else:
                        size_ = node_item
                    unit = self._get_unit(node, default_unit="micrometer")
                    # convert to meter
                    size_ = size_ * MetricSystem.from_value(unit).value
                    return size_, "m"

            mess = f"unable to find {axis} pixel size for entry {entry}"
            if self.raise_error_if_issue:
                raise ValueError(mess)
            else:
                mess += "Value will be set to default (10-6m)"
                _logger.warning(mess)
                return 10e-6, "m"

    def _get_field_of_view(self):
        if self.configuration.field_of_view is not None:
            return self.configuration.field_of_view.value
        url = self.parent_root_url() or self.root_url
        if url is None:
            return None
        with EntryReader(url) as entry:
            if self._FOV_PATH in entry:
                return h5py_read_dataset(entry[self._FOV_PATH])
            else:
                # FOV is optional: don't raise an error
                _logger.warning(
                    f"unable to find information regarding field of view for entry {entry}. set it to default value (Full)"
                )
                return "Full"

    def _update_configuration_from_tomo_config(self):
        """
        force some values from EBS tomo 'tomoconfig' group to make sure correct dataset are read
        """
        if self.configuration.ignore_bliss_tomo_config:
            return
        url = self.parent_root_url() or self.root_url
        if url is None:
            # case of entries are made manually and user do not provide an init node.
            return
        with EntryReader(url) as entry:
            technique_grp = entry.get("technique", None)
            if technique_grp is None:
                _logger.warning(
                    f"Unable to find a technique group in {entry}. Unable to reach EBStomo metadata"
                )
                return

            bliss_tomo_version = technique_grp.attrs.get("tomo_version", None)

            # read metadata
            try:
                bliss_metadata = BlissTomoConfig.from_technique_group(
                    technique_group=technique_grp
                )
            except KeyError:
                if bliss_tomo_version is not None:
                    _logger.warning(
                        f"Unable to find bliss 'tomo_config' when expected (tomo_version={bliss_tomo_version}). Fallback to conversion based on list of paths to check"
                    )
            else:
                # check if some metadata are missing
                metadata_values = {
                    "detector": bliss_metadata.tomo_detector,
                    "sample_x": bliss_metadata.sample_x,
                    "sample_y": bliss_metadata.sample_y,
                    "translation_z": bliss_metadata.translation_z,
                    "rotation": bliss_metadata.rotation,
                }
                missing_metadata = list(
                    [k for k, v in metadata_values.items() if v is None]
                )
                _logger.info(f"read tomo config from bliss. Get {metadata_values}")
                if len(missing_metadata) > 0:
                    _logger.warning(
                        f"couldn't find {missing_metadata} in bliss 'technique/tomoconfig' dataset"
                    )

                if bliss_metadata.tomo_detector is not None:
                    self.configuration.valid_camera_names = bliss_metadata.tomo_detector
                if bliss_metadata.sample_x is not None:
                    self.configuration.sample_x_keys = bliss_metadata.sample_x
                if bliss_metadata.sample_y is not None:
                    self.configuration.sample_y_keys = bliss_metadata.sample_y
                if bliss_metadata.translation_y is not None:
                    self.configuration.translation_y_keys = bliss_metadata.translation_y
                if bliss_metadata.translation_z is not None:
                    self.configuration.translation_z_keys = bliss_metadata.translation_z
                if bliss_metadata.rotation is not None:
                    self.configuration.rotation_angle_keys = bliss_metadata.rotation

    def to_NXtomos(self, request_input, input_callback, check_tomo_n=True) -> tuple:
        self._update_configuration_from_tomo_config()
        self._preprocess_registered_entries()

        nx_tomo = NXtomo()

        # 1. root level information
        # start and end time
        nx_tomo.start_time = self._get_start_time()
        nx_tomo.end_time = self._get_end_time()

        # title
        nx_tomo.title = self._get_dataset_name()
        # group size
        nx_tomo.group_size = self._get_grp_size()

        # 2. define beam
        try:
            energy, unit = self._get_user_settable_parameter(
                param_key=TomoHDF5Config.EXTRA_PARAMS_ENERGY_DK,
                fallback_fct=self._get_energy,
                dtype=float,
                input_callback=input_callback,
                ask_if_0=request_input,
            )
        except TypeError:
            # if the path lead to unexpected dataset (group instead of a dataset or a broken folder)
            _logger.error("Fail to get energy")
            energy = None
            unit = None

        if energy is not None:
            # TODO: better manamgent of energy ? might be energy.beam or energy.instrument.beam ?
            nx_tomo.energy = energy
            nx_tomo.energy.unit = unit

        # 3. define instrument
        nx_tomo.instrument.name = self._get_instrument_name()
        nx_tomo.instrument.detector.data = self._virtual_sources
        nx_tomo.instrument.detector.image_key_control = self.image_key_control
        nx_tomo.instrument.detector.count_time = self._acq_expo_time
        nx_tomo.instrument.detector.count_time.unit = "s"
        nx_tomo.instrument.detector.roi = self.get_detector_roi()
        # sample - detector distance
        try:
            sample_detector_distance, unit = self._get_user_settable_parameter(
                param_key=TomoHDF5Config.EXTRA_PARAMS_SAMPLE_DETECTOR_DISTANCE,
                fallback_fct=self._get_sample_detector_distance,
                dtype=float,
            )
        except TypeError:
            # if the path lead to unexpected dataset (group instead of a dataset or a broken folder)
            _logger.error("Fail to get sample/detector distance")
            sample_detector_distance = None
            unit = None
        if sample_detector_distance is not None:
            nx_tomo.instrument.detector.distance = sample_detector_distance
            if nx_tomo.instrument.detector.distance is not None:
                nx_tomo.instrument.detector.distance.unit = unit
        # source - sample detector distance
        try:
            source_sample_distance, unit = self._get_user_settable_parameter(
                param_key=TomoHDF5Config.EXTRA_PARAMS_SOURCE_SAMPLE_DISTANCE,
                fallback_fct=self._get_source_sample_distance,
                dtype=float,
            )
        except TypeError:
            # if the path lead to unexpected dataset (group instead of a dataset or a broken folder)
            _logger.error("Fail to get source/sample distance")
            source_sample_distance = None
            unit = None
        if source_sample_distance is not None:
            nx_tomo.instrument.source.distance = source_sample_distance
            if nx_tomo.instrument.source.distance is not None:
                nx_tomo.instrument.source.distance.unit = unit
        # x and y pixel size
        try:
            x_pixel_size, unit = self._get_user_settable_parameter(
                param_key=TomoHDF5Config.EXTRA_PARAMS_X_PIXEL_SIZE_DK,
                fallback_fct=self._get_pixel_size,
                dtype=float,
                axis="x",
            )
        except TypeError:
            # if the path lead to unexpected dataset (group instead of a dataset or a broken folder)
            _logger.error("Fail to get x_pixel_size")
            unit = None
            x_pixel_size = None
        else:
            nx_tomo.instrument.detector.x_pixel_size = x_pixel_size
        if unit is not None:
            nx_tomo.instrument.detector.x_pixel_size.unit = unit

        try:
            y_pixel_size, unit = self._get_user_settable_parameter(
                param_key=TomoHDF5Config.EXTRA_PARAMS_Y_PIXEL_SIZE_DK,
                fallback_fct=self._get_pixel_size,
                dtype=float,
                axis="y",
            )
        except TypeError:
            # if the path lead to unexpected dataset (group instead of a dataset or a broken folder)
            _logger.error("Fail to get y_pixel_size")
            unit = None
            y_pixel_size = None
        else:
            nx_tomo.instrument.detector.y_pixel_size = y_pixel_size
        if unit is not None:
            nx_tomo.instrument.detector.y_pixel_size.unit = unit

        # flips
        nx_tomo.instrument.detector.transformations.add_transformation(
            DetZFlipTransformation(flip=self.x_flipped)
        )
        nx_tomo.instrument.detector.transformations.add_transformation(
            DetYFlipTransformation(flip=self.y_flipped)
        )

        # fov
        fov = self._get_field_of_view()
        if fov is not None:
            nx_tomo.instrument.detector.field_of_view = fov

        # TODO Missing calibration mechanism from Bliss
        if self.translation_y is None or len(self.translation_y) < 1:
            _logger.warning("Unable to find translation_y")
        elif x_pixel_size is not None:
            translation_y_m = self.translation_y[
                0
            ]  # This is very fragile, no idea how to make it better
            nx_tomo.instrument.detector.x_rotation_axis_pixel_position = (
                translation_y_m / x_pixel_size
            )

        # define tomo_n
        nx_tomo.instrument.detector.tomo_n = self._get_tomo_n()

        # 4. define nx source
        source_name = self._get_source_name()
        nx_tomo.instrument.source.name = source_name
        source_type = self._get_source_type()
        if source_type is not None:
            if "synchrotron" in source_type.lower():
                source_type = SourceType.SYNCHROTRON_X_RAY_SOURCE.value
            # drop a warning if the source type is invalid
            if source_type not in SourceType.values():
                _logger.warning(
                    f"Source type ({source_type}) is not a 'standard value'"
                )

        nx_tomo.instrument.source.type = source_type

        # 5. define sample
        nx_tomo.sample.name = self._get_sample_name()
        nx_tomo.sample.rotation_angle = self.rotation_angle
        nx_tomo.sample.x_translation.value = self.sample_x
        nx_tomo.sample.x_translation.unit = "m"
        nx_tomo.sample.y_translation.value = self.sample_y
        nx_tomo.sample.y_translation.unit = "m"
        nx_tomo.sample.z_translation.value = self.translation_z
        nx_tomo.sample.z_translation.unit = "m"

        # 6. define control
        if (
            self.configuration.handle_machine_current
            and self.known_machine_electric_current not in (None, dict())
        ):
            nx_tomo.control.data = deduce_machine_current(
                timestamps=self._frames_timestamp,
                known_machine_current=self._known_machine_electric_current,
            )
            nx_tomo.control.data.unit = ElectricCurrentSystem.AMPERE
            types = set()
            if nx_tomo.control.data.value is not None:
                for d in nx_tomo.control.data.value:
                    types.add(type(d))

        if check_tomo_n:
            self.check_tomo_n()
        return (nx_tomo,)

    def check_tomo_n(self):
        # check scan is complete
        tomo_n = self._get_tomo_n()
        if self.configuration.check_tomo_n and tomo_n is not None:
            image_key_control = numpy.asarray(self._image_key_control)
            proj_found = len(
                image_key_control[image_key_control == ImageKey.PROJECTION.value]
            )
            if proj_found < tomo_n:
                mess = f"Incomplete scan. Expect {tomo_n} projection but only {proj_found} found"
                if self.configuration.raises_error is True:
                    raise ValueError(mess)
                else:
                    _logger.error(mess)

    def _check_has_metadata(self, url: DataUrl | None = None):
        url = url or self.root_url
        if url is None:
            raise ValueError(
                "no initialization entry specify, unable to" "retrieve energy"
            )

    def _get_user_settable_parameter(
        self,
        param_key,
        fallback_fct,
        dtype: type | None = None,
        *fallback_args,
        **fallback_kwargs,
    ):
        """
        return value, unit
        """
        value = self.get_already_defined_params(param_key)
        if value is not None:
            unit = TomoHDF5Config.get_extra_params_default_unit(param_key)
        else:
            value, unit = fallback_fct(*fallback_args, **fallback_kwargs)

        if dtype is None or value is None:
            return value, unit
        else:
            return dtype(value), unit
