"""Dataset-level constants for a pipeline run."""
from enum import Enum

from dkist_processing_common.models.constants import BudName
from dkist_processing_common.models.constants import ConstantsBase


class DlnirspBudName(Enum):
    """Names to be used for DLNIRSP buds."""

    arm_id = "ARM_ID"
    num_beams = "NUM_BEAMS"
    num_dsps_repeats = "NUM_DSPS_REPEATS"  # TODO: Maybe we don't need this?
    num_dither_steps = "NUM_DITHER_STEPS"
    num_mosaic_repeats = "NUM_MOSAIC_REPEATS"
    num_spatial_steps_X = "NUM_SPATIAL_STEPS_X"
    num_spatial_steps_Y = "NUM_SPATIAL_STEPS_Y"
    num_modstates = "NUM_MODSTATES"
    wavelength = "WAVELENGTH"
    camera_readout_mode = "CAMERA_READOUT_MODE"
    polarimeter_mode = "POLARIMETER_MODE"
    time_obs_list = "TIME_OBS_LIST"
    lamp_gain_exposure_times = "LAMP_GAIN_EXPOSURE_TIMES"
    solar_gain_exposure_times = "SOLAR_GAIN_EXPOSURE_TIMES"
    polcal_exposure_times = "POLCAL_EXPOSURE_TIMES"
    observe_exposure_times = "OBSERVE_EXPOSURE_TIMES"
    non_dark_task_exposure_times = "NON_DARK_TASK_EXPOSURE_TIMES"


VIS_ARM_NAMES = ["VIS".casefold()]
IR_ARM_NAMES = ["JBand".casefold(), "HBand".casefold()]


class DlnirspConstants(ConstantsBase):
    """DLNIRSP specific constants to add to the common constants."""

    @property
    def arm_id(self) -> str:
        """Arm used to record the data, either VIS or one of 2 IR bands."""
        return self._db_dict[DlnirspBudName.arm_id]

    @property
    def is_ir_data(self) -> bool:
        """Return True if the data are from an IR camera and need to be linearized."""
        if self.arm_id.casefold() in VIS_ARM_NAMES:
            return False
        if self.arm_id.casefold() in IR_ARM_NAMES:
            return True
        raise ValueError(f"Unable to determine the camera type of Arm ID {self.arm_id}")

    @property
    def num_beams(self) -> int:
        """Determine the number of beams present in the data."""
        return 2

    @property
    def num_slits(self) -> int:
        """Return the number of slits on a single detector readout."""
        return 4

    @property
    def num_dither_steps(self) -> int:
        """Return the number of dither steps."""
        return self._db_dict[DlnirspBudName.num_dither_steps]

    @property
    def num_mosaic_repeats(self) -> int:
        """
        Return the number of mosaic repeats.

        I.e., the number of times the mosaic pattern was observed.
        """
        return self._db_dict[DlnirspBudName.num_mosaic_repeats]

    @property
    def num_spatial_steps_X(self) -> int:
        """Return the number of spatial steps in the X direction in the mosaic pattern."""
        return self._db_dict[DlnirspBudName.num_spatial_steps_X]

    @property
    def num_spatial_steps_Y(self) -> int:
        """Return the number of spatial steps in the Y direction in the mosaic pattern."""
        return self._db_dict[DlnirspBudName.num_spatial_steps_Y]

    @property
    def num_mosaic_tiles(self) -> int:
        """Return the total number of tiles that make up the full mosaic."""
        return self.num_spatial_steps_X * self.num_spatial_steps_Y

    @property
    def num_cs_steps(self):
        """Find the number of calibration sequence steps."""
        return self._db_dict[BudName.num_cs_steps]

    @property
    def time_obs_list(self) -> list[str]:
        """Construct a list of all the dateobs for this dataset."""
        return self._db_dict[DlnirspBudName.time_obs_list]

    @property
    def wavelength(self) -> float:
        """Wavelength."""
        return self._db_dict[DlnirspBudName.wavelength]

    @property
    def camera_readout_mode(self) -> str:
        """Determine the readout mode of the camera."""
        return self._db_dict[DlnirspBudName.camera_readout_mode]

    @property
    def correct_for_polarization(self) -> bool:
        """Return True if dataset is polarimetric."""
        # TODO: Check what the option "Other" for DLPOLMD means
        return self._db_dict[DlnirspBudName.polarimeter_mode] == "Full Stokes"

    @property
    def lamp_gain_exposure_times(self) -> list[float]:
        """Construct a list of lamp gain FPA exposure times for the dataset."""
        return self._db_dict[DlnirspBudName.lamp_gain_exposure_times]

    @property
    def solar_gain_exposure_times(self) -> list[float]:
        """Construct a list of solar gain FPA exposure times for the dataset."""
        return self._db_dict[DlnirspBudName.solar_gain_exposure_times]

    @property
    def polcal_exposure_times(self) -> list[float]:
        """Construct a list of polcal FPA exposure times for the dataset."""
        if self.correct_for_polarization:
            return self._db_dict[DlnirspBudName.polcal_exposure_times]
        else:
            return []

    @property
    def observe_exposure_times(self) -> list[float]:
        """Construct a list of observe FPA exposure times."""
        return self._db_dict[DlnirspBudName.observe_exposure_times]

    @property
    def non_dark_task_exposure_times(self) -> list[float]:
        """Return a list of all exposure times required for all tasks other than dark."""
        exposure_times = list()
        exposure_times.extend(self.lamp_gain_exposure_times)
        exposure_times.extend(self.solar_gain_exposure_times)
        exposure_times.extend(self.observe_exposure_times)
        exposure_times = list(set(exposure_times))
        return exposure_times

    @property
    def num_modstates(self) -> int:
        """Return the number of modulator states."""
        return self._db_dict[DlnirspBudName.num_modstates]
