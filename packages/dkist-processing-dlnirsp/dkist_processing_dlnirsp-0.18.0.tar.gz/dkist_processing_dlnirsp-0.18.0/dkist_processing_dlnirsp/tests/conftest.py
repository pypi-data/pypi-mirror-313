import json
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import is_dataclass
from datetime import datetime
from functools import partial
from random import randint
from typing import Literal
from typing import Type

import numpy as np
import pytest
from astropy import coordinates
from astropy.io import fits
from astropy.time import Time
from astropy.time import TimeDelta
from astropy.wcs import WCS
from dkist_data_simulator.dataset import key_function
from dkist_data_simulator.spec122 import Spec122Dataset
from dkist_header_validator.translator import translate_spec122_to_spec214_l0
from dkist_processing_common.codecs.asdf import asdf_encoder
from dkist_processing_common.codecs.fits import fits_array_encoder
from dkist_processing_common.models.task_name import TaskName
from dkist_processing_common.tasks import WorkflowTaskBase

from dkist_processing_dlnirsp.models.constants import DlnirspConstants
from dkist_processing_dlnirsp.models.parameters import DlnirspParameters
from dkist_processing_dlnirsp.models.tags import DlnirspTag


@pytest.fixture()
def recipe_run_id():
    return randint(0, 99999)


@dataclass
class WavelengthParameter:
    values: tuple
    wavelength: tuple = (854.0, 1083.0, 1565.0)  # This must always be in order

    def __hash__(self):
        return hash((self.values, self.wavelength))


@dataclass
class FileParameter:
    """For parameters that are files on disk."""

    param_path: str
    is_file: bool = True
    objectKey: str = "not_used_because_its_already_converted"
    bucket: str = "not_used_because_we_dont_transfer"
    # Note: we have these as already-parsed file parameter (i.e., no "__file__") mainly because it allows us to have
    #       parameter files that are outside of the workflow basepath (where they would not be able to be tagged with
    #       PARAMETER_FILE). This is a pattern that we see in grogu testing.
    #       A downside of this approach is that we are slightly more fragile to changes in the underlying __file__ parsing
    #       in `*-common`. Apologies to any future devs who run into this problem. To fix it you'll need to make
    #       downstream fixtures aware of the actual files so they can be tagged prior to the instantiation of the
    #       Parameter object on some Task.

    def __hash__(self):
        return hash((self.param_path, self.is_file, self.objectKey, self.bucket))


@pytest.fixture(scope="session")
def testing_wavelength() -> float:
    return 1565.0


@dataclass
class DlnirspTestingParameters:
    dlnirsp_lamp_despike_kernel: tuple = (1, 5)
    dlnirsp_lamp_despike_threshold: float = 0.3
    dlnirsp_group_id_file_vis: FileParameter = FileParameter(param_path=".")
    dlnirsp_group_id_file_jband: FileParameter = FileParameter(param_path=".")
    dlnirsp_group_id_file_hband: FileParameter = FileParameter(param_path=".")
    dlnirsp_group_id_max_drift_px: int = 10
    dlnirsp_group_id_rough_slit_separation_px: float = 12.0
    dlnirsp_corrections_max_nan_frac: float = 0.05
    dlnirsp_geo_dispersion_file_vis: FileParameter = FileParameter(param_path=".")
    dlnirsp_geo_dispersion_file_jband: FileParameter = FileParameter(param_path=".")
    dlnirsp_geo_dispersion_file_hband: FileParameter = FileParameter(param_path=".")
    dlnirsp_geo_spectral_edge_trim: int = 1
    dlnirsp_geo_continuum_smoothing_sigma_px: float = 10.0
    dlnirsp_geo_max_shift_px: float = 100.0
    dlnirsp_geo_shift_poly_fit_order: int = 2
    dlnirsp_geo_slitbeam_fit_sig_clip: int = 3
    dlnirsp_geo_bad_px_sigma_threshold: float = 4.0
    dlnirsp_geo_reference_wave_min_nonnan_frac: float = 0.05
    dlnirsp_solar_characteristic_spectra_normalization_percentage_vis: float = 90.0
    dlnirsp_solar_characteristic_spectra_normalization_percentage_jband: float = 50.0
    dlnirsp_solar_characteristic_spectra_normalization_percentage_hband: float = 50.0
    dlnirsp_polcal_demodulation_spatial_poly_fit_order: int = 2
    dlnirsp_polcal_demodulation_fit_sig_clip: float = 3.0
    dlnirsp_polcal_demodulation_fit_max_niter: int = 10
    dlnirsp_polcal_metrics_num_sample_points: int = 100
    dlnirsp_max_cs_step_time_sec: float = 180.0
    dlnirsp_pac_remove_linear_I_trend: bool = True
    dlnirsp_pac_fit_mode: str = "use_M12_I_sys_per_step"
    dlnirsp_pac_init_set: str = "OCCal_VIS"
    dlnirsp_ifu_x_pos_file_vis: FileParameter = FileParameter(param_path=".")
    dlnirsp_ifu_x_pos_file_jband: FileParameter = FileParameter(param_path=".")
    dlnirsp_ifu_x_pos_file_hband: FileParameter = FileParameter(param_path=".")
    dlnirsp_ifu_y_pos_file_vis: FileParameter = FileParameter(param_path=".")
    dlnirsp_ifu_y_pos_file_jband: FileParameter = FileParameter(param_path=".")
    dlnirsp_ifu_y_pos_file_hband: FileParameter = FileParameter(param_path=".")


@dataclass
class DlnirspTestingConstants:
    INSTRUMENT: str = "DLNIRSP"
    OBS_IP_START_TIME: str = "2024-06-06"
    ARM_ID: str = "HBand"
    NUM_MODSTATES: int = 8
    NUM_SPATIAL_STEPS_X: int = 2
    NUM_SPATIAL_STEPS_Y: int = 3
    NUM_DITHER_STEPS: int = 1
    NUM_MOSAIC_REPEATS: int = 4
    NUM_CS_STEPS: int = 7
    WAVELENGTH: float = 1565.0
    CAM_READOUT_MODE: str = "UpTheRamp"
    POLARIMETER_MODE: str = "Full Stokes"
    TIME_OBS_LIST: tuple[str] = ("2023-02-09T00:02:27.562", "2023-02-09T00:02:27.630")
    LAMP_GAIN_EXPOSURE_TIMES: tuple[float] = (100.0,)
    SOLAR_GAIN_EXPOSURE_TIMES: tuple[float] = (1.0,)
    POLCAL_EXPOSURE_TIMES: tuple[float] = (1.0,)
    OBSERVE_EXPOSURE_TIMES: tuple[float] = (2.0,)
    AVERAGE_CADENCE: float = 10.0
    MINIMUM_CADENCE: float = 11.0
    MAXIMUM_CADENCE: float = 12.0
    VARIANCE_CADENCE: float = 3.0
    CONTRIBUTING_PROPOSAL_IDS: tuple[str] = (
        "PROPID1",
        "PROPID2",
    )
    CONTRIBUTING_EXPERIMENT_IDS: tuple[str] = (
        "EXPERID1",
        "EXPERID2",
        "EXPERID3",
    )


@pytest.fixture(scope="session")
def session_recipe_run_id():
    return randint(0, 99999)


@pytest.fixture(scope="session")
def session_link_constants_db():
    return constants_linker


@pytest.fixture
def link_constants_db():
    return constants_linker


def constants_linker(recipe_run_id: int, constants_obj):
    """Take a dataclass (or dict) containing a constants DB and link it to a specific recipe run id."""
    if is_dataclass(constants_obj):
        constants_obj = asdict(constants_obj)
    constants = DlnirspConstants(recipe_run_id=recipe_run_id, task_name="test")
    constants._purge()
    constants._update(constants_obj)
    return


@pytest.fixture(scope="session")
def input_dataset_document_simple_parameters_part():
    def get_input_dataset_parameters_part(parameters: DlnirspTestingParameters):
        parameters_list = []
        value_id = randint(1000, 2000)
        for pn, pv in asdict(parameters).items():
            if type(pv) is WavelengthParameter:
                pv = asdict(pv)
            values = [
                {
                    "parameterValueId": value_id,
                    "parameterValue": json.dumps(pv),
                    "parameterValueStartDate": "1946-11-20",  # Remember Duane Allman
                }
            ]
            parameter = {"parameterName": pn, "parameterValues": values}
            parameters_list.append(parameter)
        return parameters_list

    return get_input_dataset_parameters_part


@pytest.fixture(scope="session")
def default_arm_id() -> str:
    return "JBand"


@pytest.fixture(scope="session")
def default_obs_ip_start_time() -> str:
    return "2024-06-06"


@pytest.fixture(scope="session")
def assign_input_dataset_doc_to_task(
    input_dataset_document_simple_parameters_part,
    testing_wavelength,
    default_arm_id,
    default_obs_ip_start_time,
):
    def update_task(
        task,
        parameters,
        parameter_class=DlnirspParameters,
        arm_id: str = default_arm_id,
        obs_ip_start_time: str = default_obs_ip_start_time,
    ):
        doc_path = task.scratch.workflow_base_path / "dataset_parameters.json"
        with open(doc_path, "w") as f:
            f.write(json.dumps(input_dataset_document_simple_parameters_part(parameters)))
        task.tag(doc_path, DlnirspTag.input_dataset_parameters())
        task.parameters = parameter_class(
            task.input_dataset_parameters,
            obs_ip_start_time=obs_ip_start_time,
            wavelength=testing_wavelength,
            arm_id=arm_id,
        )

    return update_task


def compute_telgeom(time_hst: Time):
    dkist_lon = (156 + 15 / 60.0 + 21.7 / 3600.0) * (-1)
    dkist_lat = 20 + 42 / 60.0 + 27.0 / 3600.0
    hel = 3040.4
    hloc = coordinates.EarthLocation.from_geodetic(dkist_lon, dkist_lat, hel)
    sun_body = coordinates.get_body("sun", time_hst, hloc)  # get the solar ephemeris
    azel_frame = coordinates.AltAz(obstime=time_hst, location=hloc)  # Horizon coords
    sun_altaz = sun_body.transform_to(azel_frame)  # Sun in horizon coords
    alt = sun_altaz.alt.value  # Extract altitude
    azi = sun_altaz.az.value  # Extract azimuth

    tableang = alt - azi

    return {"TELEVATN": alt, "TAZIMUTH": azi, "TTBLANGL": tableang}


@pytest.fixture
def modulation_matrix() -> np.ndarray:
    # From SJ
    return np.array(
        [
            [1.0, 0.3850679, -0.47314817, -0.79238554],
            [1.0, 0.55357905, 0.51096333, -0.43773452],
            [1.0, -0.43053245, 0.67947448, 0.17335161],
            [1.0, -0.5990436, -0.30463702, 0.68287954],
            [1.0, 0.3850679, -0.47314817, 0.79238554],
            [1.0, 0.55357905, 0.51096333, 0.43773452],
            [1.0, -0.43053245, 0.67947448, -0.17335161],
            [1.0, -0.5990436, -0.30463702, -0.68287954],
        ]
    )


@pytest.fixture
def demodulation_matrix(modulation_matrix) -> np.ndarray:
    return np.linalg.pinv(modulation_matrix)


class DlnirspHeaders(Spec122Dataset):
    def __init__(
        self,
        dataset_shape: tuple[int, ...],
        array_shape: tuple[int, ...],
        time_delta: float = 10.0,
        instrument: str = "dlnirsp",
        polarimeter_mode: str = "Full Stokes",
        arm_id: str = "HBand",
        dither_mode_on: bool = False,
        dither_step: bool = False,
        **kwargs,
    ):
        if len(array_shape) == 2:
            array_shape = (1, *array_shape)
        super().__init__(
            dataset_shape=dataset_shape,
            array_shape=array_shape,
            time_delta=time_delta,
            instrument=instrument,
            **kwargs,
        )
        self.add_constant_key("WAVELNTH", 1565.0)
        self.add_constant_key("DLN__001", arm_id)
        self.add_constant_key("DLN__046", "UpTheRamp")
        self.add_constant_key("DLN__014", 8)
        self.add_constant_key("ID___013", "TEST_PROPOSAL_ID")
        self.add_constant_key("DLN__008", polarimeter_mode)
        self.add_constant_key("ID___012", "TEST_EXP_ID")
        self.add_constant_key("DLN__008", "Full Stokes")
        self.add_constant_key("DLN__042", dither_mode_on)

        if dither_mode_on:
            self.add_constant_key("DLN__045", dither_step)
        else:
            self.add_remove_key("DLN__045")

        if arm_id == "VIS":
            # Remove keys that only appear in IR camera headers
            for i in range(46, 55):
                self.add_remove_key(f"DLN__{i:03n}")

    @property
    def fits_wcs(self):
        w = WCS(naxis=self.array_ndim)
        w.wcs.crpix = self.array_shape[2] / 2, self.array_shape[1] / 2, 1
        w.wcs.crval = 1565.0, 0, 0
        w.wcs.cdelt = 0.2, 1, 1
        w.wcs.cunit = "nm", "arcsec", "arcsec"
        w.wcs.ctype = "AWAV", "HPLT-TAN", "HPLN-TAN"
        w.wcs.pc = np.identity(self.array_ndim)
        return w


class RawRampHeaders(DlnirspHeaders):
    def __init__(
        self,
        array_shape: tuple[int, ...],
        num_ramps: int,
        num_line: int,
        num_read: int,
        num_reset: int,
        num_coadd: int = 1,
        start_date: str = "2023-01-01T01:23:45",
        ramp_length_sec: float = 1.0,
        arm_id: str = "HBand",
    ):
        if len(array_shape) == 3:
            if array_shape[0] != 1:
                raise ValueError(f"{array_shape = } is weird")
            array_shape = array_shape[1:]

        self.num_frames_per_coadd = num_line + num_read
        num_NDR_per_ramp = self.num_frames_per_coadd * num_coadd + num_reset
        num_frames = num_ramps * num_NDR_per_ramp
        dataset_shape = (num_frames, *array_shape)
        super().__init__(dataset_shape=dataset_shape, array_shape=array_shape, arm_id=arm_id)
        self.num_NDR_per_ramp = num_NDR_per_ramp
        self.start_date = Time(start_date)
        self.ramp_length_sec = TimeDelta(ramp_length_sec, format="sec")
        self.num_coadd = num_coadd
        self.num_line = num_line
        self.num_read = num_read
        self.num_reset = num_reset

        coadd_read_sequence = f"{num_line}line,{num_read}read"
        cam_read_sequence = ",".join([coadd_read_sequence] * num_coadd)

        if num_reset > 0:
            cam_read_sequence += f",{num_reset}line"

        self.add_constant_key("DLN__049", num_NDR_per_ramp)
        self.add_constant_key("DLN__047", cam_read_sequence)

        self.ms_per_NDR = ramp_length_sec / num_coadd / num_read * 1000

    @property
    def current_ramp(self) -> int:
        return self.index // self.num_NDR_per_ramp

    @property
    def current_coadd_in_ramp(self) -> int:
        index_in_ramp = self.frame_in_ramp("") - 1
        if index_in_ramp < self.num_NDR_per_ramp - self.num_reset:
            return index_in_ramp // self.num_frames_per_coadd
        return -1  # Is a reset

    @property
    def frame_in_coadd(self) -> int:
        index_in_ramp = self.frame_in_ramp("") - 1
        if index_in_ramp < self.num_NDR_per_ramp - self.num_reset:
            return index_in_ramp % self.num_frames_per_coadd
        return -1  # Is a reset

    @key_function("DLN__050")
    def frame_in_ramp(self, key: str) -> int:
        return (self.index % self.num_NDR_per_ramp) + 1

    @key_function("DATE-OBS")
    def date_obs(self, key: str) -> str:
        ramp_time = self.start_date + self.ramp_length_sec * self.current_ramp
        return ramp_time.fits

    @key_function("CAM__004")
    def coadd_exp_time(self, key: str) -> float:
        if self.frame_in_coadd < self.num_line:
            # This captures bias/line frames and resets (-1)
            return 0.0
        return self.ramp_length_sec.value / self.num_coadd * 1000

    @key_function("CAM__005")
    def NDR_exp_time(self, key: str) -> float:
        if self.frame_in_coadd < self.num_line:
            # This captures bias/line frames and resets (-1)
            return 0.0
        return self.ms_per_NDR


class AbortedRampHeaders(RawRampHeaders):
    def __init__(
        self,
        array_shape: tuple[int, ...],
        num_line: int,
        num_read: int,
        num_reset: int,
        start_date: str,
    ):
        super().__init__(
            array_shape=array_shape,
            num_ramps=1,
            num_line=num_line,
            num_read=num_read,
            num_reset=num_reset,
            start_date=start_date,
        )
        full_dataset_shape = self.dataset_shape
        aborted_dataset_shape = (full_dataset_shape[0] - 1, *full_dataset_shape[1:])
        super(RawRampHeaders, self).__init__(
            dataset_shape=aborted_dataset_shape, array_shape=array_shape
        )
        self.add_constant_key("DLN__049", num_line + num_read + num_reset)


class BadNumFramesPerRampHeaders(RawRampHeaders):
    def __init__(
        self,
        array_shape: tuple[int, ...],
        num_line: int,
        num_read: int,
        num_reset: int,
        start_date: str,
    ):
        super().__init__(
            array_shape=array_shape,
            num_ramps=1,
            num_line=num_line,
            num_read=num_read,
            num_reset=num_reset,
            start_date=start_date,
        )
        del self._fixed_keys["DLN__049"]

    @key_function("DLN__049")
    def wrong_num_NDR_per_ramp(self, key: str) -> int:
        return self.index


class SimpleModulatedHeaders(DlnirspHeaders):
    def __init__(
        self,
        num_modstates: int,
        array_shape: tuple[int, ...],
        task: str,
        exp_time_ms: float,
        start_date: str = "2023-01-01T01:23:45",
        modstate_length_sec: float = 0.5,
        arm_id: str = "JBand",
    ):
        if len(array_shape) == 3:
            if array_shape[0] != 1:
                raise ValueError(f"{array_shape = } is weird")
            array_shape = array_shape[1:]
        dataset_shape = (num_modstates, *array_shape)
        super().__init__(
            dataset_shape=dataset_shape,
            array_shape=array_shape,
            start_time=datetime.fromisoformat(start_date),
            time_delta=modstate_length_sec,
            arm_id=arm_id,
        )

        self.add_constant_key("DKIST004", task)
        self.add_constant_key("DLN__014", num_modstates)
        self.add_constant_key("CAM__004", exp_time_ms)

    @key_function("DLN__015")
    def current_modstate(self, key: str) -> int:
        return self.index + 1


class ModulatedLampGainHeaders(SimpleModulatedHeaders):
    def __init__(
        self,
        num_modstates: int,
        array_shape: tuple[int, ...],
        exp_time_ms: float,
        start_date: str = "2023-01-01T01:23:45",
        modstate_length_sec: float = 0.5,
    ):
        super().__init__(
            num_modstates=num_modstates,
            array_shape=array_shape,
            task="gain",
            exp_time_ms=exp_time_ms,
            start_date=start_date,
            modstate_length_sec=modstate_length_sec,
        )

        self.add_constant_key("PAC__002", "lamp")
        self.add_constant_key("PAC__003", "on")


class ModulatedSolarGainHeaders(SimpleModulatedHeaders):
    def __init__(
        self,
        num_modstates: int,
        array_shape: tuple[int, ...],
        exp_time_ms: float,
        start_date: str = "2023-01-01T01:23:45",
        modstate_length_sec: float = 0.5,
    ):
        super().__init__(
            num_modstates=num_modstates,
            array_shape=array_shape,
            task="gain",
            exp_time_ms=exp_time_ms,
            start_date=start_date,
            modstate_length_sec=modstate_length_sec,
        )

        self.add_constant_key("PAC__002", "clear")
        self.add_constant_key("PAC__003", "undefined")


class ModulatedCSStepHeaders(SimpleModulatedHeaders):
    def __init__(
        self,
        num_modstates: int,
        pol_status: str,
        pol_theta: float,
        ret_status: str,
        ret_theta: float,
        dark_status: str,
        cs_step_num: int,
        array_shape: tuple[int, ...],
        exp_time_ms: float,
        start_date: str = "2023-01-01T01:23:45",
        modstate_length_sec: float = 0.5,
    ):
        super().__init__(
            num_modstates=num_modstates,
            array_shape=array_shape,
            task="polcal",
            exp_time_ms=exp_time_ms,
            start_date=start_date,
            modstate_length_sec=modstate_length_sec,
        )

        self.cs_step_num = (
            cs_step_num  # This doesn't become a header key, but helps with making fake data
        )
        self.pol_status = pol_status
        self.pol_theta = pol_theta
        self.ret_status = ret_status
        self.ret_theta = ret_theta
        self.dark_status = dark_status

    @key_function("PAC__004")
    def polarizer_status(self, key: str) -> str:
        return self.pol_status

    @key_function("PAC__005")
    def polarizer_angle(self, key: str) -> float | str:
        return "none" if self.pol_status == "clear" else self.pol_theta

    @key_function("PAC__006")
    def retarder_status(self, key: str) -> str:
        return self.ret_status

    @key_function("PAC__007")
    def retarder_angle(self, key: str) -> float | str:
        return "none" if self.ret_status == "clear" else self.ret_theta

    @key_function("PAC__008")
    def gos_level3_status(self, key: str) -> str:
        return self.dark_status

    @key_function("TAZIMUTH", "TELEVATN", "TTBLANGL")
    def telescope_geometry(self, key: str):
        return compute_telgeom(Time(self.date_obs(key), format="fits"))[key]


@pytest.fixture(scope="session")
def small_calibration_sequence() -> tuple[list, ...]:
    # Make up a Calibration sequence. Mostly random except for two clears and two darks at start and end, which
    # we want to test
    pol_status = [
        "clear",
        "clear",
        "Sapphire Polarizer",
        "Sapphire Polarizer",
        "Sapphire Polarizer",
        "clear",
        "clear",
    ]
    pol_theta = [0.0, 0.0, 60.0, 0.0, 120.0, 0.0, 0.0]
    ret_status = ["clear", "clear", "clear", "SiO2 SAR", "clear", "clear", "clear"]
    ret_theta = [0.0, 0.0, 0.0, 45.0, 0.0, 0.0, 0.0]
    dark_status = [
        "DarkShutter",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "DarkShutter",
    ]

    return pol_status, pol_theta, ret_status, ret_theta, dark_status


class ModulatedObserveHeaders(DlnirspHeaders):
    def __init__(
        self,
        num_modstates: int,
        num_mosaics: int,
        num_X_tiles: int,
        num_Y_tiles: int,
        num_data_cycles: int,
        array_shape: tuple[int, ...],
        exp_time_ms: float,
        dither_mode_on: bool = False,
        start_date: str = "2023-01-01T01:23:45",
        modstate_length_sec: float = 0.5,
        allow_3D_arrays: bool = False,
    ):
        if len(array_shape) == 3 and not allow_3D_arrays:
            if array_shape[0] != 1:
                raise ValueError(f"{array_shape = } is weird")
            array_shape = array_shape[1:]

        num_dither = int(dither_mode_on) + 1
        num_files = (
            num_mosaics * num_dither * num_X_tiles * num_Y_tiles * num_data_cycles * num_modstates
        )

        self.dither_bool_list = sum(
            [
                [
                    bool(d)
                    for _ in range(num_X_tiles * num_Y_tiles * num_data_cycles * num_modstates)
                ]
                for d in range(num_dither)
            ]
            * num_mosaics,
            [],
        )
        self.modstate_id_list = (
            list(range(1, num_modstates + 1))
            * num_mosaics
            * num_dither
            * num_X_tiles
            * num_Y_tiles
            * num_data_cycles
        )
        self.data_cycle_id_list = sum(
            [[i for _ in range(num_modstates)] for i in range(1, num_data_cycles + 1)]
            * num_Y_tiles
            * num_X_tiles
            * num_dither
            * num_mosaics,
            [],
        )
        self.Y_tile_id_list = (
            sum(
                [[i for _ in range(num_modstates * num_data_cycles)] for i in range(num_Y_tiles)]
                * num_X_tiles
                * num_mosaics,
                [],
            )
            * num_dither
        )
        self.X_tile_id_list = sum(
            [
                [i for _ in range(num_modstates * num_data_cycles * num_Y_tiles)]
                for i in range(num_X_tiles)
            ]
            * num_mosaics
            * num_dither,
            [],
        )
        self.mosaic_id_list = sum(
            [
                [
                    i
                    for _ in range(
                        num_modstates * num_data_cycles * num_Y_tiles * num_X_tiles * num_dither
                    )
                ]
                for i in range(num_mosaics)
            ],
            [],
        )

        dataset_shape = (num_files, *array_shape)
        super().__init__(
            dataset_shape=dataset_shape,
            array_shape=array_shape,
            start_time=datetime.fromisoformat(start_date),
            time_delta=modstate_length_sec,
            dither_mode_on=dither_mode_on,
        )

        self.add_constant_key("DKIST004", "OBSERVE")
        self.add_constant_key("DLN__031", num_mosaics)
        self.add_constant_key("DLN__034", num_X_tiles)
        self.add_constant_key("DLN__038", num_Y_tiles)
        self.add_constant_key("DLN__020", num_data_cycles)
        self.add_constant_key("DLN__014", num_modstates)
        self.add_constant_key("CAM__004", exp_time_ms)
        if dither_mode_on:
            del self._fixed_keys["DLN__045"]

    @key_function("DLN__045")
    def current_dither(self, key: str) -> bool:
        return self.dither_bool_list[self.index]

    @key_function("DLN__032")
    def current_mosaic(self, key: str) -> int:
        return self.mosaic_id_list[self.index]

    @key_function("DLN__037")
    def current_X_tile(self, key: str) -> int:
        return self.X_tile_id_list[self.index]

    @key_function("DLN__041")
    def current_Y_tile(self, key: str) -> int:
        return self.Y_tile_id_list[self.index]

    @key_function("DLN__021")
    def current_data_cycle(self, key: str) -> int:
        return self.data_cycle_id_list[self.index]

    @key_function("DLN__015")
    def current_modstate(self, key: str) -> int:
        return self.modstate_id_list[self.index]


class AbortedMosaicObserveHeaders(ModulatedObserveHeaders):
    """For observe data where an abort was issued at given instrument loop."""

    def __init__(
        self,
        num_mosaics: int,
        num_X_tiles: int,
        num_Y_tiles: int,
        num_data_cycles: int,
        num_modstates: int,
        dither_mode_on: bool = False,
        aborted_loop_level: Literal[
            "dither", "mosaic", "X_tile", "Y_tile", "data_cycle", "modstate"
        ]
        | None = "dither",
        first_XY_loop: Literal["X", "Y"] = "X",
        array_shape: tuple[int, ...] = (10, 10),
        exp_time_ms: float = 6.0,
        start_date: str = "2023-01-01T01:23:45",
        modstate_length_sec: float = 0.5,
    ):

        if len(array_shape) == 3:
            if array_shape[0] != 1:
                raise ValueError(f"{array_shape = } is weird")
            array_shape = array_shape[1:]

        num_dither = int(dither_mode_on) + 1
        num_files = (
            num_dither * num_mosaics * num_X_tiles * num_Y_tiles * num_data_cycles * num_modstates
        )

        self.dither_bool_list = sum(
            [
                [
                    bool(d)
                    for _ in range(num_X_tiles * num_Y_tiles * num_data_cycles * num_modstates)
                ]
                for d in range(num_dither)
            ]
            * num_mosaics,
            [],
        )
        self.modstate_id_list = (
            list(range(1, num_modstates + 1))
            * num_mosaics
            * num_dither
            * num_X_tiles
            * num_Y_tiles
            * num_data_cycles
        )
        self.data_cycle_id_list = sum(
            [[i for _ in range(num_modstates)] for i in range(1, num_data_cycles + 1)]
            * num_Y_tiles
            * num_X_tiles
            * num_dither
            * num_mosaics,
            [],
        )
        self.Y_tile_id_list = self.get_Y_tile_id_list(
            first_XY_loop=first_XY_loop,
            num_modstates=num_modstates,
            num_data_cycles=num_data_cycles,
            num_Y_tiles=num_Y_tiles,
            num_X_tiles=num_X_tiles,
            num_mosaics=num_mosaics,
            num_dither=num_dither,
        )
        self.X_tile_id_list = self.get_X_tile_id_list(
            first_XY_loop=first_XY_loop,
            num_modstates=num_modstates,
            num_data_cycles=num_data_cycles,
            num_Y_tiles=num_Y_tiles,
            num_X_tiles=num_X_tiles,
            num_mosaics=num_mosaics,
            num_dither=num_dither,
        )
        self.mosaic_id_list = sum(
            [
                [
                    i
                    for _ in range(
                        num_modstates * num_dither * num_X_tiles * num_Y_tiles * num_data_cycles
                    )
                ]
                for i in range(num_mosaics)
            ],
            [],
        )

        match aborted_loop_level:
            case "mosaic":
                num_missing_files = (
                    num_dither * num_X_tiles * num_Y_tiles * num_data_cycles * num_modstates
                )

            case "dither":
                num_missing_files = num_X_tiles * num_Y_tiles * num_data_cycles * num_modstates

            case "X_tile":
                num_missing_files = num_data_cycles * num_modstates
                if first_XY_loop == "X":
                    num_missing_files *= num_Y_tiles

            case "Y_tile":
                num_missing_files = num_data_cycles * num_modstates
                if first_XY_loop == "Y":
                    num_missing_files *= num_X_tiles

            case "data_cycle":
                num_missing_files = num_modstates

            case "modstate":
                num_missing_files = 1

            case _:
                num_missing_files = 0

        num_files -= num_missing_files

        # Not strictly necessary to shorten these lists because by setting num_files correctly
        # we'll never index into the ends of the full lists, but it helps make things clear
        # (and provides assurance we never accidentally make more files than we expected).
        if num_missing_files > 0:
            self.modstate_id_list = self.modstate_id_list[:-num_missing_files]
            self.Y_tile_id_list = self.Y_tile_id_list[:-num_missing_files]
            self.X_tile_id_list = self.X_tile_id_list[:-num_missing_files]
            self.mosaic_id_list = self.mosaic_id_list[:-num_missing_files]
            self.dither_bool_list = self.dither_bool_list[:-num_missing_files]

        dataset_shape = (num_files, *array_shape)
        super(ModulatedObserveHeaders, self).__init__(
            dataset_shape=dataset_shape,
            array_shape=array_shape,
            start_time=datetime.fromisoformat(start_date),
            time_delta=modstate_length_sec,
            dither_mode_on=dither_mode_on,
        )

        self.add_constant_key("DKIST004", "OBSERVE")
        self.add_constant_key("DLN__031", num_mosaics)
        self.add_constant_key("DLN__034", num_X_tiles)
        self.add_constant_key("DLN__038", num_Y_tiles)
        self.add_constant_key("DLN__020", num_data_cycles)
        self.add_constant_key("DLN__014", num_modstates)
        self.add_constant_key("CAM__004", exp_time_ms)
        if dither_mode_on:
            del self._fixed_keys["DLN__045"]

    def get_Y_tile_id_list(
        self,
        first_XY_loop: Literal["X", "Y"],
        num_modstates: int,
        num_data_cycles: int,
        num_Y_tiles: int,
        num_X_tiles: int,
        num_mosaics: int,
        num_dither: int,
    ) -> list[int]:
        inner_range = num_modstates * num_data_cycles
        output_repeat = num_mosaics * num_dither * num_X_tiles
        if first_XY_loop == "Y":
            inner_range *= num_X_tiles
            output_repeat //= num_X_tiles

        return sum(
            [[i for _ in range(inner_range)] for i in range(num_Y_tiles)] * output_repeat, []
        )

    def get_X_tile_id_list(
        self,
        first_XY_loop: Literal["X", "Y"],
        num_modstates: int,
        num_data_cycles: int,
        num_Y_tiles: int,
        num_X_tiles: int,
        num_mosaics: int,
        num_dither: int,
    ) -> list[int]:
        inner_range = num_modstates * num_data_cycles * num_Y_tiles
        output_repeat = num_mosaics * num_dither
        if first_XY_loop == "Y":
            inner_range //= num_Y_tiles
            output_repeat *= num_Y_tiles
        return sum(
            [[i for _ in range(inner_range)] for i in range(num_X_tiles)] * output_repeat,
            [],
        )


class MissingMosaicStepObserveHeaders(ModulatedObserveHeaders):
    """For headers where the set of `mosaic_num` values isn't continuous."""

    def __init__(self, array_shape: tuple[int, ...]):

        super().__init__(
            num_modstates=2,
            num_mosaics=2,
            num_X_tiles=3,
            num_Y_tiles=3,
            num_data_cycles=2,
            array_shape=array_shape,
            dither_mode_on=True,
            exp_time_ms=6.0,
        )

        self.mosaic_id_list = [i * 2 for i in self.mosaic_id_list]


class MissingDitherStepObserveHeaders(ModulatedObserveHeaders):
    """For headers where the set of `dither_num` values isn't continuous."""

    def __init__(self, array_shape: tuple[int, ...], num_mosaics: int = 1):

        super().__init__(
            num_modstates=2,
            num_mosaics=num_mosaics,
            num_X_tiles=3,
            num_Y_tiles=3,
            num_data_cycles=2,
            dither_mode_on=True,
            array_shape=array_shape,
            exp_time_ms=6.0,
        )

        self.dither_bool_list = [True for _ in self.dither_bool_list]


class MissingXStepObserveHeaders(ModulatedObserveHeaders):
    """For headers where the set of `X_tile_num` values isn't continuous."""

    def __init__(self, array_shape: tuple[int, ...], num_mosaics: int = 1):
        """Set num_mosaics > 1 to test whole missing X tiles in the middle of all mosaics."""

        super().__init__(
            num_modstates=2,
            num_mosaics=num_mosaics,
            num_X_tiles=3,
            num_Y_tiles=2,
            num_data_cycles=2,
            array_shape=array_shape,
            exp_time_ms=6.0,
        )

        self.X_tile_id_list = [i * 2 for i in self.X_tile_id_list]


class MissingYStepObserveHeaders(ModulatedObserveHeaders):
    """For headers where the set of `Y_tile_num` values isn't continuous."""

    def __init__(self, array_shape: tuple[int, ...], num_mosaics: int = 1, num_X_tiles: int = 1):
        """Set either num_mosaics > 1 or num_X_tiles > 1 to test whole missing Y tiles from all higher-level loops."""
        super().__init__(
            num_modstates=2,
            num_mosaics=num_mosaics,
            num_X_tiles=num_X_tiles,
            num_Y_tiles=3,
            num_data_cycles=2,
            array_shape=array_shape,
            exp_time_ms=6.0,
        )

        self.Y_tile_id_list = [i * 2 for i in self.Y_tile_id_list]


class CalibratedHeaders(ModulatedObserveHeaders):
    def __init__(
        self,
        num_mosaics: int,
        num_X_tiles: int,
        num_Y_tiles: int,
        is_polarimetric: bool,
        dither_mode_on: bool = False,
        array_shape: tuple[int, int, int] = (3, 4, 5),
    ):

        # Use the data_cycles loop to represent Stokes parameters
        num_stokes = 4 if is_polarimetric else 1

        super().__init__(
            num_mosaics=num_mosaics,
            num_X_tiles=num_X_tiles,
            num_Y_tiles=num_Y_tiles,
            num_data_cycles=num_stokes,
            num_modstates=1,
            array_shape=array_shape,
            dither_mode_on=dither_mode_on,
            exp_time_ms=1.0,
            allow_3D_arrays=True,
        )

        self.stokes_name_list = ["I", "Q", "U", "V"]
        self.add_constant_key("DLN__014", 8 if is_polarimetric else 1)
        self.add_constant_key("DLN__008", "Full Stokes" if is_polarimetric else "Stokes I")

        # These are added during the Science task
        self.add_constant_key("DATE-END", "2023-01-01T02:34:56")
        if is_polarimetric:
            self.add_constant_key("POL_NOIS", 0.4)
            self.add_constant_key("POL_SENS", 1.4)

    @property
    def current_stokes(self) -> str:
        stokes_axis_id = (
            self.data_cycle_id_list[self.index] - 1
        )  # -1 b/c data cycles are indexed from 1
        return self.stokes_name_list[stokes_axis_id]

    @property
    def fits_wcs(self):
        w = WCS(naxis=3)
        w.wcs.crpix = self.array_shape[2] / 2, self.array_shape[1] / 2, self.array_shape[0] / 2
        w.wcs.crval = 666.0, 999.0, 1565.0
        w.wcs.cdelt = 1, 1, 0.2
        w.wcs.cunit = "arcsec", "arcsec", "nm"
        w.wcs.ctype = "HPLT-TAN", "HPLN-TAN", "AWAV"
        w.wcs.pc = np.identity(self.array_ndim)
        return w


class MovieFrameHeaders(ModulatedObserveHeaders):
    def __init__(
        self,
        num_mosaics: int,
        num_X_tiles: int,
        num_Y_tiles: int,
        dither_mode_on: bool = False,
        array_shape: tuple[int, int] = (4, 5),
    ):
        if len(array_shape) != 2:
            raise ValueError(f"Only 2D movie frames are allowed. Got shape {array_shape}")

        super().__init__(
            num_mosaics=num_mosaics,
            num_X_tiles=num_X_tiles,
            num_Y_tiles=num_Y_tiles,
            num_data_cycles=1,
            num_modstates=1,
            array_shape=array_shape,
            exp_time_ms=1.0,
            dither_mode_on=dither_mode_on,
        )


def make_random_data(frame: Spec122Dataset) -> np.ndarray:
    shape = frame.array_shape[1:]
    data = np.random.random(shape)

    return data


def make_3D_random_data(frame: CalibratedHeaders) -> np.ndarray:
    shape = frame.array_shape
    data = np.random.random(shape)

    return data


def make_cs_data(
    frame: ModulatedCSStepHeaders, dark_signal: float, clear_signal: float
) -> np.ndarray:

    shape = frame.array_shape[1:]
    clear_signal += frame.current_modstate("dummy_arg")
    if frame.pol_status == "clear" and frame.ret_status == "clear":
        if frame.dark_status == "DarkShutter":
            value = dark_signal
        else:
            value = clear_signal + dark_signal
    else:
        value = (
            frame.cs_step_num * 10000.0 + frame.current_modstate("dummy_arg") * 100.0
        ) * clear_signal + dark_signal

    data = np.ones(shape) * value

    return data


def tag_on_modstate(frame: Spec122Dataset) -> list[str]:
    modstate = frame.header()["DLN__015"]
    return [DlnirspTag.modstate(modstate)]


def tag_obs_on_mosaic_dither_modstate(frame: ModulatedObserveHeaders) -> list[str]:
    modstate = frame.current_modstate("foo")
    X_tile = frame.current_X_tile("foo")
    Y_tile = frame.current_Y_tile("foo")
    mosaic = frame.current_mosaic("foo")
    # Because we tag an `int`, but the header value is `bool`
    dither = int(frame.current_dither("foo"))
    return [
        DlnirspTag.modstate(modstate),
        DlnirspTag.tile_X_num(X_tile),
        DlnirspTag.tile_Y_num(Y_tile),
        DlnirspTag.dither_step(dither),
        DlnirspTag.mosaic_num(mosaic),
    ]


def tag_on_mosaic_dither_stokes(frame: CalibratedHeaders) -> list[str]:
    mosaic = frame.current_mosaic("foo")
    # Because we tag an `int`, but the header value is `bool`
    dither = int(frame.current_dither("foo"))
    X_tile = frame.current_X_tile("foo")
    Y_tile = frame.current_Y_tile("foo")
    stokes = frame.current_stokes

    return [
        DlnirspTag.mosaic_num(mosaic),
        DlnirspTag.dither_step(dither),
        DlnirspTag.tile_X_num(X_tile),
        DlnirspTag.tile_Y_num(Y_tile),
        DlnirspTag.stokes(stokes),
    ]


def tag_on_mosaic_dither_loops(frame: MovieFrameHeaders) -> list[str]:
    mosaic = frame.current_mosaic("foo")
    # Because we tag an `int`, but the header value is `bool`
    dither = int(frame.current_dither("foo"))
    X_tile = frame.current_X_tile("foo")
    Y_tile = frame.current_Y_tile("foo")

    return [
        DlnirspTag.mosaic_num(mosaic),
        DlnirspTag.dither_step(dither),
        DlnirspTag.tile_X_num(X_tile),
        DlnirspTag.tile_Y_num(Y_tile),
    ]


def write_frames_to_task(
    task: Type[WorkflowTaskBase],
    frame_generator: Spec122Dataset,
    data_func: callable = make_random_data,
    extra_tags: list[str] | None = None,
    tag_func: callable = lambda x: [],
):
    if not extra_tags:
        extra_tags = []
    tags = [DlnirspTag.frame()] + extra_tags

    num_frames = 0
    for frame in frame_generator:
        header = frame.header()
        data = data_func(frame)
        frame_tags = tags + tag_func(frame)
        translated_header = fits.Header(translate_spec122_to_spec214_l0(header))
        task.write(data=data, header=translated_header, tags=frame_tags, encoder=fits_array_encoder)
        num_frames += 1

    return num_frames


def write_simple_frames_to_task(
    task: Type[WorkflowTaskBase],
    task_type: str,
    exp_time_ms: float = 10.0,
    num_modstates: int = 8,
    array_shape: tuple[int, int] = (10, 10),
    data_func: callable = make_random_data,
    tags: list[str] | None = None,
    tag_func: callable = lambda x: [],
) -> int:

    frame_generator = SimpleModulatedHeaders(
        num_modstates=num_modstates,
        array_shape=array_shape,
        task=task_type,
        exp_time_ms=exp_time_ms,
    )

    num_frames = write_frames_to_task(
        task=task,
        frame_generator=frame_generator,
        data_func=data_func,
        extra_tags=tags,
        tag_func=tag_func,
    )

    return num_frames


def write_dark_frames_to_task(
    task: Type[WorkflowTaskBase],
    exp_time_ms: float,
    num_modstates: int = 8,
    array_shape: tuple[int, int] = (10, 10),
    data_func: callable = make_random_data,
    tags: list[str] | None = None,
) -> int:

    frame_generator = SimpleModulatedHeaders(
        num_modstates=num_modstates, array_shape=array_shape, task="dark", exp_time_ms=exp_time_ms
    )

    num_frames = write_frames_to_task(
        task=task, frame_generator=frame_generator, data_func=data_func, extra_tags=tags
    )

    return num_frames


def write_lamp_gain_frames_to_task(
    task: Type[WorkflowTaskBase],
    exp_time_ms: float = 10.0,
    num_modstates: int = 8,
    array_shape: tuple[int, int] = (10, 10),
    data_func: callable = make_random_data,
    tags: list[str] | None = None,
    tag_func: callable = lambda x: [],
) -> int:

    frame_generator = ModulatedLampGainHeaders(
        num_modstates=num_modstates, array_shape=array_shape, exp_time_ms=exp_time_ms
    )

    num_frames = write_frames_to_task(
        task=task,
        frame_generator=frame_generator,
        data_func=data_func,
        extra_tags=tags,
        tag_func=tag_func,
    )

    return num_frames


def write_solar_gain_frames_to_task(
    task: Type[WorkflowTaskBase],
    exp_time_ms: float = 5.0,
    num_modstates: int = 8,
    array_shape: tuple[int, int] = (10, 10),
    data_func: callable = make_random_data,
    tags: list[str] | None = None,
    tag_func: callable = lambda x: [],
) -> int:

    frame_generator = ModulatedSolarGainHeaders(
        num_modstates=num_modstates, array_shape=array_shape, exp_time_ms=exp_time_ms
    )

    num_frames = write_frames_to_task(
        task=task,
        frame_generator=frame_generator,
        data_func=data_func,
        extra_tags=tags,
        tag_func=tag_func,
    )

    return num_frames


def write_geometric_calibration_to_task(
    task: Type[WorkflowTaskBase],
    shift_dict: dict[int, np.ndarray],
    scale_dict: dict[int, np.ndarray],
    wave_axis: np.ndarray,
):

    tree = {
        "spectral_shifts": shift_dict,
        "spectral_scales": scale_dict,
        "reference_wavelength_axis": wave_axis,
    }
    task.write(
        data=tree,
        tags=[DlnirspTag.intermediate(), DlnirspTag.task_geometric()],
        encoder=asdf_encoder,
    )

    return


def write_calibration_sequence_frames(
    task: Type[WorkflowTaskBase],
    pol_status: list[str],
    pol_theta: list[float],
    ret_status: list[str],
    ret_theta: list[float],
    dark_status: list[str],
    exp_time: float = 7.0,
    dark_signal: float = 5.0,
    clear_signal: float = 10.0,
    array_shape: tuple[int, ...] = (10, 10),
    data_func: callable = None,
    tags: list[str] | None = None,
) -> int:
    if data_func is None:
        data_func = partial(make_cs_data, dark_signal=dark_signal, clear_signal=clear_signal)

    num_frames = 0
    for step, (pol_s, pol_t, ret_s, ret_t, dark_s) in enumerate(
        zip(pol_status, pol_theta, ret_status, ret_theta, dark_status)
    ):
        dataset = ModulatedCSStepHeaders(
            num_modstates=8,
            pol_status=pol_s,
            pol_theta=pol_t,
            ret_status=ret_s,
            ret_theta=ret_t,
            dark_status=dark_s,
            cs_step_num=step,
            array_shape=array_shape,
            exp_time_ms=exp_time,
        )

        step_tags = list(set(tags + [DlnirspTag.cs_step(step), DlnirspTag.task_polcal()]))

        if pol_s == "clear" and ret_s == "clear":
            if dark_s == "DarkShutter":
                step_tags += [DlnirspTag.task_polcal_dark()]
            else:
                step_tags += [DlnirspTag.task_polcal_gain()]

        num_frames += write_frames_to_task(
            task=task,
            frame_generator=dataset,
            data_func=data_func,
            extra_tags=step_tags,
            tag_func=tag_on_modstate,
        )

    return num_frames


def write_observe_frames_to_task(
    task: Type[WorkflowTaskBase],
    exp_time_ms: float = 6.0,
    num_modstates: int = 8,
    num_X_tiles: int = 2,
    num_Y_tiles: int = 3,
    num_mosaics: int = 4,
    num_data_cycles: int = 2,
    dither_mode_on: bool = False,
    array_shape: tuple[int, int] = (10, 10),
    data_func: callable = make_random_data,
    tags: list[str] | None = None,
    tag_func: callable = lambda x: [],
) -> int:

    frame_generator = ModulatedObserveHeaders(
        num_modstates=num_modstates,
        num_X_tiles=num_X_tiles,
        num_Y_tiles=num_Y_tiles,
        num_mosaics=num_mosaics,
        num_data_cycles=num_data_cycles,
        array_shape=array_shape,
        exp_time_ms=exp_time_ms,
        dither_mode_on=dither_mode_on,
    )

    num_frames = write_frames_to_task(
        task=task,
        frame_generator=frame_generator,
        data_func=data_func,
        extra_tags=tags,
        tag_func=tag_func,
    )

    return num_frames


def write_polcal_frames_to_task(
    task: Type[WorkflowTaskBase],
    exp_time_ms: float = 7.0,
    num_modstates: int = 8,
    array_shape: tuple[int, int] = (10, 10),
    data_func: callable = make_random_data,
    tags: list[str] | None = None,
) -> int:

    frame_generator = SimpleModulatedHeaders(
        num_modstates=num_modstates,
        array_shape=array_shape,
        task=TaskName.polcal.value,
        exp_time_ms=exp_time_ms,
    )

    num_frames = write_frames_to_task(
        task=task, frame_generator=frame_generator, data_func=data_func, extra_tags=tags
    )

    return num_frames


def write_calibrated_frames_to_task(
    task,
    num_mosaics: int,
    num_X_tiles: int,
    num_Y_tiles: int,
    is_polarimetric: bool,
    array_shape: tuple[int, int, int],
    dither_mode_on: bool = False,
    data_func: callable = make_3D_random_data,
):
    dataset = CalibratedHeaders(
        num_mosaics=num_mosaics,
        num_X_tiles=num_X_tiles,
        num_Y_tiles=num_Y_tiles,
        is_polarimetric=is_polarimetric,
        dither_mode_on=dither_mode_on,
        array_shape=array_shape,
    )

    num_written_frames = write_frames_to_task(
        task=task,
        frame_generator=dataset,
        extra_tags=[DlnirspTag.calibrated(), DlnirspTag.frame()],
        tag_func=tag_on_mosaic_dither_stokes,
        data_func=data_func,
    )
    return num_written_frames


@pytest.fixture
def slit_borders() -> list[tuple[int, int]]:
    return [(1, 12), (14, 25), (28, 39)]


@pytest.fixture
def num_slits(slit_borders) -> int:
    return len(slit_borders)


@pytest.fixture
def num_slitbeams(num_slits) -> int:
    return num_slits * 2


@pytest.fixture
def groups_in_slitbeams(group_id_array, num_slits, num_groups_per_slitbeam):
    num_groups = int(np.nanmax(group_id_array) + 1)
    group_list = list(range(num_groups))
    num_slitbeams = num_slits * 2
    return {
        s: [group_list.pop(0) for _ in range(num_groups_per_slitbeam)] for s in range(num_slitbeams)
    }


@pytest.fixture
def num_groups_per_slitbeam() -> int:
    # See group_id_array below for why this is 3
    return 3


@pytest.fixture
def group_id_array(slit_borders) -> np.ndarray:
    array = np.empty((10, 40)) * np.nan

    for slit, (low, high) in enumerate(slit_borders):
        array[1:3, low:high] = 0 + (6 * slit)
        array[4:6, low:high] = 2 + (6 * slit)
        array[7:9, low:high] = 4 + (6 * slit)

        mid = (low + high) // 2
        array[:, mid:high] += 1
        array[:, mid - 1 : mid + 2] = np.nan

    return array


@pytest.fixture
def vis_group_id_array(group_id_array):
    return group_id_array


@pytest.fixture
def jband_group_id_array(group_id_array):
    return group_id_array


@pytest.fixture
def hband_group_id_array(group_id_array):
    return group_id_array


@pytest.fixture
def ifu_x_pos_array(group_id_array):
    x_pos_array = np.copy(group_id_array)
    x_pos_array /= x_pos_array  # Convert all non-NaN to 1.
    x_pos_array *= np.arange(x_pos_array.shape[0])[:, None]

    return x_pos_array


@pytest.fixture
def ifu_y_pos_array(group_id_array):
    y_pos_array = np.copy(group_id_array)
    y_pos_array /= y_pos_array  # Convert all non-NaN to 1.
    y_pos_array *= np.arange(y_pos_array.shape[1])[None, :]

    return y_pos_array


@pytest.fixture
def vis_ifu_x_pos_array(ifu_x_pos_array):
    return ifu_x_pos_array * 10.0


@pytest.fixture
def vis_ifu_y_pos_array(ifu_y_pos_array):
    return ifu_y_pos_array * 10.0


@pytest.fixture
def jband_ifu_x_pos_array(ifu_x_pos_array):
    return ifu_x_pos_array * 13.0


@pytest.fixture
def jband_ifu_y_pos_array(ifu_y_pos_array):
    return ifu_y_pos_array * 13.0


@pytest.fixture
def hband_ifu_x_pos_array(ifu_x_pos_array):
    return ifu_x_pos_array * 15.0


@pytest.fixture
def hband_ifu_y_pos_array(ifu_y_pos_array):
    return ifu_y_pos_array * 15.0


@pytest.fixture
def num_groups(group_id_array) -> int:
    return int(np.nanmax(group_id_array) + 1)


@pytest.fixture
def array_with_groups(group_id_array, num_groups) -> np.ndarray:

    array = np.empty(group_id_array.shape)

    for g in range(num_groups):
        idx = np.where(group_id_array == g)
        array[idx] = g * 100.0

    return array


@pytest.fixture
def vis_group_id_file_parameter(vis_group_id_array, tmp_path) -> FileParameter:
    file_path = tmp_path / "group_ids_vis.fits"
    fits.PrimaryHDU(vis_group_id_array).writeto(file_path)

    return FileParameter(param_path=str(file_path))


@pytest.fixture
def jband_group_id_file_parameter(jband_group_id_array, tmp_path) -> FileParameter:
    file_path = tmp_path / "group_ids_jband.fits"
    fits.PrimaryHDU(jband_group_id_array).writeto(file_path)

    return FileParameter(param_path=str(file_path))


@pytest.fixture
def hband_group_id_file_parameter(hband_group_id_array, tmp_path) -> FileParameter:
    file_path = tmp_path / "group_ids_hband.fits"
    fits.PrimaryHDU(hband_group_id_array).writeto(file_path)

    return FileParameter(param_path=str(file_path))


@pytest.fixture
def vis_ifu_x_pos_file_parameter(vis_ifu_x_pos_array, tmp_path) -> FileParameter:
    file_path = tmp_path / "ifu_x_pos_vis.fits"
    fits.PrimaryHDU(vis_ifu_x_pos_array).writeto(file_path)

    return FileParameter(param_path=str(file_path))


@pytest.fixture
def vis_ifu_y_pos_file_parameter(vis_ifu_y_pos_array, tmp_path) -> FileParameter:
    file_path = tmp_path / "ifu_y_pos_vis.fits"
    fits.PrimaryHDU(vis_ifu_y_pos_array).writeto(file_path)

    return FileParameter(param_path=str(file_path))


@pytest.fixture
def jband_ifu_x_pos_file_parameter(jband_ifu_x_pos_array, tmp_path) -> FileParameter:
    file_path = tmp_path / "ifu_x_pos_jband.fits"
    fits.PrimaryHDU(jband_ifu_x_pos_array).writeto(file_path)

    return FileParameter(param_path=str(file_path))


@pytest.fixture
def jband_ifu_y_pos_file_parameter(jband_ifu_y_pos_array, tmp_path) -> FileParameter:
    file_path = tmp_path / "ifu_y_pos_jband.fits"
    fits.PrimaryHDU(jband_ifu_y_pos_array).writeto(file_path)

    return FileParameter(param_path=str(file_path))


@pytest.fixture
def hband_ifu_x_pos_file_parameter(hband_ifu_x_pos_array, tmp_path) -> FileParameter:
    file_path = tmp_path / "ifu_x_pos_hband.fits"
    fits.PrimaryHDU(hband_ifu_x_pos_array).writeto(file_path)

    return FileParameter(param_path=str(file_path))


@pytest.fixture
def hband_ifu_y_pos_file_parameter(hband_ifu_y_pos_array, tmp_path) -> FileParameter:
    file_path = tmp_path / "ifu_y_pos_hband.fits"
    fits.PrimaryHDU(hband_ifu_y_pos_array).writeto(file_path)

    return FileParameter(param_path=str(file_path))


@pytest.fixture
def vis_dispersion_array(vis_group_id_array) -> np.ndarray:
    dispersion_offset = 4000.0  # Angstrom/px
    return vis_group_id_array * 10 + dispersion_offset


@pytest.fixture
def jband_dispersion_array(jband_group_id_array):
    dispersion_offset = 4000.0  # Angstrom/px
    return jband_group_id_array * 10 + dispersion_offset


@pytest.fixture
def hband_dispersion_array(hband_group_id_array):
    dispersion_offset = 4000.0  # Angstrom/px
    return hband_group_id_array * 10 + dispersion_offset


@pytest.fixture
def vis_dispersion_file_parameter(vis_dispersion_array, tmp_path) -> FileParameter:
    file_path = tmp_path / "dispersions_vis.fits"
    fits.PrimaryHDU(vis_dispersion_array).writeto(file_path)
    return FileParameter(param_path=str(file_path))


@pytest.fixture
def jband_dispersion_file_parameter(jband_dispersion_array, tmp_path) -> FileParameter:
    file_path = tmp_path / "dispersions_jband.fits"
    fits.PrimaryHDU(jband_dispersion_array).writeto(file_path)
    return FileParameter(param_path=str(file_path))


@pytest.fixture
def hband_dispersion_file_parameter(hband_dispersion_array, tmp_path) -> FileParameter:
    file_path = tmp_path / "dispersions_hband.fits"
    fits.PrimaryHDU(hband_dispersion_array).writeto(file_path)
    return FileParameter(param_path=str(file_path))


@pytest.fixture
def write_drifted_group_ids_to_task(jband_group_id_array):
    # Use jband because that's what all the tests use
    def writer(task):
        task.write(
            data=jband_group_id_array,
            tags=[
                DlnirspTag.intermediate(),
                DlnirspTag.frame(),
                DlnirspTag.task_drifted_ifu_groups(),
            ],
            encoder=fits_array_encoder,
        )

    return writer


@pytest.fixture
def reference_wave_axis(group_id_array) -> np.ndarray:
    # Mostly made up. We want it to be smaller than the full array, but larger than a slitbeam
    return np.arange(group_id_array.shape[1] // 3)


@pytest.fixture
def shifts_and_scales(
    num_groups,
) -> tuple[dict[int, np.ndarray], dict[int, np.ndarray], int, float]:
    shift_amount = 1
    scale_amount = 1.0

    # This length of these arrays just has to be longer than a single group's spatial size
    shift_dict = {g: np.ones(40) * shift_amount for g in range(num_groups)}
    scale_dict = {g: np.ones(40) * scale_amount for g in range(num_groups)}

    return shift_dict, scale_dict, shift_amount, scale_amount


@pytest.fixture
def constants_class_with_different_num_slits(num_slits) -> Type[DlnirspConstants]:
    class ConstantsWithDifferentSlits(DlnirspConstants):
        @property
        def num_slits(self) -> int:
            return num_slits

    return ConstantsWithDifferentSlits


@pytest.fixture
def polcal_quality_beam_labels() -> list[str]:
    return ["Beam 1", "Beam 2"]


@pytest.fixture
def polcal_quality_skip_constants(polcal_quality_beam_labels) -> list[bool]:
    return ["1" not in label for label in polcal_quality_beam_labels]
