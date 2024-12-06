"""Custom parsers to identify task sub-groupings not captured by a single header key."""
from typing import Type

from dkist_processing_common.models.flower_pot import SpilledDirt
from dkist_processing_common.models.tags import StemName
from dkist_processing_common.models.task_name import TaskName
from dkist_processing_common.parsers.single_value_single_key_flower import (
    SingleValueSingleKeyFlower,
)

from dkist_processing_dlnirsp.parsers.dlnirsp_l0_fits_access import DlnirspL0FitsAccess


def parse_header_ip_task(fits_obj: DlnirspL0FitsAccess) -> str:
    """
    Parse DLNIRSP tasks from a combination of header values.

    Parameters
    ----------
    fits_obj:
        A single FitsAccess object
    """
    # Distinguish between lamp and solar gains
    if (
        fits_obj.ip_task_type == "gain"
        and fits_obj.gos_level3_status == "lamp"
        and fits_obj.gos_level3_lamp_status == "on"
    ):
        return TaskName.lamp_gain.value
    if fits_obj.ip_task_type == "gain" and fits_obj.gos_level3_status == "clear":
        return TaskName.solar_gain.value

    # Everything else is unchanged
    return fits_obj.ip_task_type


def parse_polcal_task_type(fits_obj: DlnirspL0FitsAccess) -> str | Type[SpilledDirt]:
    """Identify and tag polcal dark and gain frames."""
    if (
        fits_obj.gos_level0_status == "DarkShutter"
        and fits_obj.gos_retarder_status == "clear"
        and fits_obj.gos_polarizer_status == "clear"
    ):
        return TaskName.polcal_dark.value

    elif (
        fits_obj.gos_level0_status.startswith("FieldStop")
        and fits_obj.gos_retarder_status == "clear"
        and fits_obj.gos_polarizer_status == "clear"
    ):
        return TaskName.polcal_gain.value

    # We don't care about a POLCAL frame that is neither dark nor clear
    return SpilledDirt


class DlnirspTaskTypeFlower(SingleValueSingleKeyFlower):
    """Flower to find the DLNIRSP task type."""

    def __init__(self):
        super().__init__(tag_stem_name=StemName.task.value, metadata_key="ip_task_type")

    def setter(self, fits_obj: DlnirspL0FitsAccess):
        """
        Set value of the flower.

        Parameters
        ----------
        fits_obj:
            A single FitsAccess object
        """
        return parse_header_ip_task(fits_obj)


class PolcalTaskFlower(SingleValueSingleKeyFlower):
    """
    Flower to find the polcal task type.

    This is separate from the "main" task-type flower because we still need all polcal frames to be tagged
    with just POLCAL (which is what the main task-type flower does); this flower adds an extra task tag for
    just POLCA_DARK and POLCAL_GAIN frames, but those frames are still POLCAL frames, too.
    """

    def __init__(self):
        super().__init__(tag_stem_name=StemName.task.value, metadata_key="ip_task_type")

    def setter(self, fits_obj: DlnirspL0FitsAccess):
        """
        Set value of the flower.

        Parameters
        ----------
        fits_obj:
            A single FitsAccess object
        """
        if fits_obj.ip_task_type.upper() != TaskName.polcal.value.upper():
            return SpilledDirt

        return parse_polcal_task_type(fits_obj)
