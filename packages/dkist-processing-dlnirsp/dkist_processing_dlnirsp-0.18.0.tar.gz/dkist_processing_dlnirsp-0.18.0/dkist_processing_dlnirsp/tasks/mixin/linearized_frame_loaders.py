"""Helpers for loading specific linearized data."""
from typing import Generator

import numpy as np
from dkist_processing_common.codecs.fits import fits_access_decoder

from dkist_processing_dlnirsp.models.tags import DlnirspTag
from dkist_processing_dlnirsp.parsers.dlnirsp_l0_fits_access import DlnirspL0FitsAccess


class LinearizedFrameLoadersMixin:
    """Mixin for methods that support easy loading of linearity corrected frames."""

    def linearized_frame_loaders_fits_access_generator(
        self,
        tags: list[str],
    ) -> Generator[DlnirspL0FitsAccess, None, None]:
        """
        Load linearized fits frames.

        Returns
        -------
        A fits access generator based on the inputs provided
        """
        full_frame_generator = self.read(
            tags=tags, decoder=fits_access_decoder, fits_access_class=DlnirspL0FitsAccess
        )

        yield from full_frame_generator

    def linearized_frame_loaders_dark_array_generator(
        self,
        exposure_time: float,
    ) -> Generator[np.ndarray, None, None]:
        """
        Return a fits access generator with dark frames for the given parameters.

        Parameters
        ----------
        exposure_time
            The current exposure time

        Returns
        -------
        A fits access generator based on the inputs provided
        """
        tags = [
            DlnirspTag.linearized(),
            DlnirspTag.frame(),
            DlnirspTag.task_dark(),
            DlnirspTag.exposure_time(exposure_time),
        ]
        dark_array_fits_access = self.linearized_frame_loaders_fits_access_generator(tags=tags)
        for array in dark_array_fits_access:
            yield array.data

    def linearized_frame_loaders_lamp_gain_array_generator(
        self,
        exposure_time: float,
    ) -> Generator[np.ndarray, None, None]:
        """
        Return a fits access generator with dark frames for the given parameters.

        Parameters
        ----------
        exposure_time
            The current exposure time

        Returns
        -------
        A fits access generator based on the inputs provided
        """
        tags = [
            DlnirspTag.linearized(),
            DlnirspTag.frame(),
            DlnirspTag.task_lamp_gain(),
            DlnirspTag.exposure_time(exposure_time),
        ]
        lamp_gain_fits_access = self.linearized_frame_loaders_fits_access_generator(tags=tags)
        for array in lamp_gain_fits_access:
            yield array.data
