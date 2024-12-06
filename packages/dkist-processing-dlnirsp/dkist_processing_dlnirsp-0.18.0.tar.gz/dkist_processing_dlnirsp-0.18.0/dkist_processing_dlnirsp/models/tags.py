"""DLNIRSP-specific file tags."""
from enum import Enum

from dkist_processing_common.models.tags import Tag

from dkist_processing_dlnirsp.models.task_name import DlnirspTaskName


class DlnirspStemName(str, Enum):
    """Controlled list of Tag Stems."""

    linearized = "LINEARIZED"
    beam = "BEAM"
    arm_id = "ARM_ID"
    scan_step = "SCAN_STEP"
    current_frame_in_ramp = "CURRENT_FRAME_IN_RAMP"
    time_obs = "TIME_OBS"
    modstate = "MODSTATE"
    dither_step = "DITHER_STEP"
    mosaic_num = "MOSAIC_NUM"
    tile_X_num = "TILE_X_NUM"
    tile_Y_num = "TILE_Y_NUM"


class DlnirspTag(Tag):
    """DLNIRSP specific tag formatting."""

    @classmethod
    def beam(cls, beam_num: int) -> str:
        """
        Tags by beam number.

        Parameters
        ----------
        beam_num
            The beam number

        Returns
        -------
        The formatted tag string
        """
        return cls.format_tag(DlnirspStemName.beam, beam_num)

    @classmethod
    def modstate(cls, modstate: int) -> str:
        """
        Tags by the current modstate number.

        Parameters
        ----------
        modstate
            The current scan step number

        Returns
        -------
        The formatted tag string
        """
        return cls.format_tag(DlnirspStemName.modstate, modstate)

    @classmethod
    def linearized(cls) -> str:
        """
        Tags for linearized frames.

        Returns
        -------
        The formatted tag string
        """
        return cls.format_tag(DlnirspStemName.linearized)

    @classmethod
    def arm_id(cls, arm_id: str) -> str:
        """
        Tags based on the CryoNIRSP arm_id from which the data is recorded (SP or CI).

        Parameters
        ----------
        arm_id
            The arm ID in use, SP or CI

        Returns
        -------
        The formatted tag string
        """
        return cls.format_tag(DlnirspStemName.arm_id, arm_id)

    @classmethod
    def current_frame_in_ramp(cls, curr_frame_in_ramp: int) -> str:
        """
        Tags based on the current frame number in the ramp.

        Parameters
        ----------
        curr_frame_in_ramp
            The current frame number for this ramp

        Returns
        -------
        The formatted tag string
        """
        return cls.format_tag(DlnirspStemName.current_frame_in_ramp, curr_frame_in_ramp)

    @classmethod
    def time_obs(cls, time_obs: str) -> str:
        """
        Tags by the observe date.

        Parameters
        ----------
        time_obs
            The observe time

        Returns
        -------
        The formatted tag string
        """
        return cls.format_tag(DlnirspStemName.time_obs, time_obs)

    @classmethod
    def mosaic_num(cls, mosaic_num: int) -> str:
        """Tags by the mosaic number."""
        return cls.format_tag(DlnirspStemName.mosaic_num, mosaic_num)

    @classmethod
    def tile_X_num(cls, tile_X_num: int) -> str:
        """Tags by the current mosaic location in the X direction."""
        return cls.format_tag(DlnirspStemName.tile_X_num, tile_X_num)

    @classmethod
    def tile_Y_num(cls, tile_Y_num: int) -> str:
        """Tags by the current mosaic location in the Y direction."""
        return cls.format_tag(DlnirspStemName.tile_Y_num, tile_Y_num)

    @classmethod
    def dither_step(cls, dither_step: int) -> str:
        """Tags by dither step."""
        return cls.format_tag(DlnirspStemName.dither_step, dither_step)

    @classmethod
    def task_drifted_ifu_groups(cls) -> str:
        """Identify the IFU group ID array with drift applied."""
        return cls.task(DlnirspTaskName.drifted_ifu_group_id)

    @classmethod
    def task_drifted_dispersion(cls) -> str:
        """Identify the IFU dispersion array with drift applied."""
        return cls.task(DlnirspTaskName.drifted_dispersion)

    @classmethod
    def task_drifted_ifu_x_pos(cls) -> str:
        """Identify the IFU X Pos array with drift applied."""
        return cls.task(DlnirspTaskName.drifted_ifu_x_pos)

    @classmethod
    def task_drifted_ifu_y_pos(cls) -> str:
        """Identify the IFU Y Pos array with drift applied."""
        return cls.task(DlnirspTaskName.drifted_ifu_y_pos)
