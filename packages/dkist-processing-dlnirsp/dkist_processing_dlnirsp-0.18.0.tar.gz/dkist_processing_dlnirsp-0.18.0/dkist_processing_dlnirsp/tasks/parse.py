"""Tasks for parsing both raw and linearized data."""
from typing import TypeVar

from dkist_processing_common.models.flower_pot import Stem
from dkist_processing_common.models.task_name import TaskName
from dkist_processing_common.parsers.cs_step import CSStepFlower
from dkist_processing_common.parsers.cs_step import NumCSStepBud
from dkist_processing_common.parsers.single_value_single_key_flower import (
    SingleValueSingleKeyFlower,
)
from dkist_processing_common.parsers.time import ExposureTimeFlower
from dkist_processing_common.parsers.time import ObsIpStartTimeBud
from dkist_processing_common.parsers.time import TaskExposureTimesBud
from dkist_processing_common.parsers.unique_bud import TaskUniqueBud
from dkist_processing_common.parsers.unique_bud import UniqueBud
from dkist_processing_common.tasks import default_constant_bud_factory
from dkist_processing_common.tasks import default_tag_flower_factory
from dkist_processing_common.tasks import ParseDataBase
from dkist_processing_common.tasks.mixin.input_dataset import InputDatasetMixin

from dkist_processing_dlnirsp.models.constants import DlnirspBudName
from dkist_processing_dlnirsp.models.parameters import DlnirspParsingParameters
from dkist_processing_dlnirsp.models.tags import DlnirspStemName
from dkist_processing_dlnirsp.models.tags import DlnirspTag
from dkist_processing_dlnirsp.parsers.dlnirsp_l0_fits_access import DlnirspL0FitsAccess
from dkist_processing_dlnirsp.parsers.dlnirsp_l0_fits_access import DlnirspRampFitsAccess
from dkist_processing_dlnirsp.parsers.mosaic import NumDitherStepsBud
from dkist_processing_dlnirsp.parsers.mosaic import NumMosaicRepeatsBud
from dkist_processing_dlnirsp.parsers.mosaic import NumXTilesBud
from dkist_processing_dlnirsp.parsers.mosaic import NumYTilesBud
from dkist_processing_dlnirsp.parsers.task import DlnirspTaskTypeFlower
from dkist_processing_dlnirsp.parsers.task import parse_header_ip_task
from dkist_processing_dlnirsp.parsers.task import PolcalTaskFlower
from dkist_processing_dlnirsp.parsers.time import DlnirspTimeObsBud
from dkist_processing_dlnirsp.parsers.wavelength import ObserveWavelengthBud

S = TypeVar("S", bound=Stem)

__all__ = ["ParseL0DlnirspRampData", "ParseL0DlnirspLinearizedData"]


class ParseL0DlnirspRampData(ParseDataBase):
    """
    Parse DLNIRSP pre-linearized ramp data.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    @property
    def fits_parsing_class(self):
        """FITS access class to be used with this task."""
        return DlnirspRampFitsAccess

    @property
    def constant_buds(self) -> list[S]:
        """Add DLNIRSP specific constants to common constants."""
        return [
            UniqueBud(
                constant_name=DlnirspBudName.camera_readout_mode.value,
                metadata_key="camera_readout_mode",
            ),
            # Time Obs is the unique identifier for each ramp in the data set
            DlnirspTimeObsBud(),
            # This is used to determine whether we need to do any linearity correction at all.
            UniqueBud(constant_name=DlnirspBudName.arm_id.value, metadata_key="arm_id"),
        ]

    @property
    def tag_flowers(self) -> list[S]:
        """Add DLNIRSP specific tags to common tags."""
        return [
            SingleValueSingleKeyFlower(
                tag_stem_name=DlnirspStemName.current_frame_in_ramp.value,
                metadata_key="current_frame_in_ramp",
            ),
            # time_obs is a unique identifier for all raw frames in a single ramp
            SingleValueSingleKeyFlower(
                tag_stem_name=DlnirspStemName.time_obs.value,
                metadata_key="time_obs",
            ),
        ]

    @property
    def tags_for_input_frames(self) -> list[str]:
        """Tags for the input data to parse."""
        return [DlnirspTag.input(), DlnirspTag.frame()]


class ParseL0DlnirspLinearizedData(ParseDataBase, InputDatasetMixin):
    """
    Parse linearity corrected DLNIRSP input data.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    def __init__(
        self,
        recipe_run_id: int,
        workflow_name: str,
        workflow_version: str,
    ):
        super().__init__(
            recipe_run_id=recipe_run_id,
            workflow_name=workflow_name,
            workflow_version=workflow_version,
        )
        self.parameters = DlnirspParsingParameters(self.input_dataset_parameters)

    @property
    def fits_parsing_class(self):
        """FITS access class to be used in this task."""
        return DlnirspL0FitsAccess

    @property
    def tags_for_input_frames(self) -> list[str]:
        """Tags for the linearity corrected input frames."""
        return [DlnirspTag.linearized(), DlnirspTag.frame()]

    @property
    def constant_buds(self) -> list[S]:
        """Add DLNIRSP specific constants to common constants."""
        return default_constant_bud_factory() + [
            ObserveWavelengthBud(),
            ObsIpStartTimeBud(),
            NumCSStepBud(max_cs_step_time_sec=self.parameters.max_cs_step_time_sec),
            UniqueBud(
                constant_name=DlnirspBudName.polarimeter_mode.value, metadata_key="polarimeter_mode"
            ),
            UniqueBud(
                constant_name=DlnirspBudName.num_modstates.value,
                metadata_key="number_of_modulator_states",
            ),
            NumMosaicRepeatsBud(),
            NumDitherStepsBud(),
            NumXTilesBud(),
            NumYTilesBud(),
            TaskExposureTimesBud(
                stem_name=DlnirspBudName.lamp_gain_exposure_times.value,
                ip_task_type=TaskName.lamp_gain.value,
                header_task_parsing_func=parse_header_ip_task,
            ),
            TaskExposureTimesBud(
                stem_name=DlnirspBudName.solar_gain_exposure_times.value,
                ip_task_type=TaskName.solar_gain.value,
                header_task_parsing_func=parse_header_ip_task,
            ),
            TaskExposureTimesBud(
                stem_name=DlnirspBudName.observe_exposure_times.value,
                ip_task_type=TaskName.observe.value,
                header_task_parsing_func=parse_header_ip_task,
            ),
            TaskExposureTimesBud(
                stem_name=DlnirspBudName.polcal_exposure_times.value,
                ip_task_type=TaskName.polcal.value,
                header_task_parsing_func=parse_header_ip_task,
            ),
        ]

    @property
    def tag_flowers(self) -> list[S]:
        """Add DLNIRSP specific tags to common tags."""
        return default_tag_flower_factory() + [
            DlnirspTaskTypeFlower(),
            PolcalTaskFlower(),
            SingleValueSingleKeyFlower(
                tag_stem_name=DlnirspStemName.arm_id.value, metadata_key="arm_id"
            ),
            ExposureTimeFlower(),
            SingleValueSingleKeyFlower(
                tag_stem_name=DlnirspStemName.modstate.value, metadata_key="modulator_state"
            ),
            SingleValueSingleKeyFlower(
                tag_stem_name=DlnirspStemName.mosaic_num.value, metadata_key="mosaic_num"
            ),
            SingleValueSingleKeyFlower(
                tag_stem_name=DlnirspStemName.tile_X_num.value, metadata_key="X_tile_num"
            ),
            SingleValueSingleKeyFlower(
                tag_stem_name=DlnirspStemName.tile_Y_num.value, metadata_key="Y_tile_num"
            ),
            SingleValueSingleKeyFlower(
                tag_stem_name=DlnirspStemName.dither_step.value, metadata_key="dither_step"
            ),
            CSStepFlower(max_cs_step_time_sec=self.parameters.max_cs_step_time_sec),
        ]
