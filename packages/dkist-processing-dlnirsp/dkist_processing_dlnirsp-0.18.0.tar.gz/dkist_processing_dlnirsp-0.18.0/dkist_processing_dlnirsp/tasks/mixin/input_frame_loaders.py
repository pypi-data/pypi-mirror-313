"""Mixin for easy loading of raw input data."""
from typing import Generator

from dkist_processing_common.codecs.fits import fits_access_decoder

from dkist_processing_dlnirsp.models.tags import DlnirspTag
from dkist_processing_dlnirsp.parsers.dlnirsp_l0_fits_access import DlnirspRampFitsAccess


class InputFrameLoadersMixin:
    """Mixin for methods that support easy loading of input frames."""

    def input_frame_loaders_fits_access_generator(
        self,
        time_obs: str,
    ) -> Generator[DlnirspRampFitsAccess, None, None]:
        """
        Return a fits access generator of raw input frames based on the time-obs.

        A single time-obs should correspond to a single ramp.
        """
        tags = [DlnirspTag.input(), DlnirspTag.frame(), DlnirspTag.time_obs(time_obs)]

        frame_generator = self.read(
            tags=tags, decoder=fits_access_decoder, fits_access_class=DlnirspRampFitsAccess
        )
        return frame_generator
