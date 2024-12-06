"""List of intermediate task names."""
from enum import StrEnum


class DlnirspTaskName(StrEnum):
    """Controlled list of DLNIRSP task tag names."""

    drifted_ifu_group_id = "DRIFTED_IFU_GROUP_ID"
    drifted_dispersion = "DRIFTED_DISPERSION"
    drifted_ifu_x_pos = "DRIFTED_IFU_XPOS"
    drifted_ifu_y_pos = "DRIFTED_IFU_YPOS"
