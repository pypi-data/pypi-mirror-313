"""Helpers for writing and loading specific intermediate calibration objects."""
import itertools
from pathlib import Path
from typing import Generator
from typing import Iterable

import asdf
import numpy as np
from astropy.io import fits
from dkist_processing_common.codecs.asdf import asdf_decoder
from dkist_processing_common.codecs.fits import fits_array_decoder
from dkist_processing_common.codecs.fits import fits_array_encoder
from dkist_processing_common.models.task_name import TaskName
from dkist_service_configuration.logging import logger

from dkist_processing_dlnirsp.models.tags import DlnirspTag


class IntermediateFrameHelpersMixin:
    """Mixin for methods that support easy loading and writing of intermediate frames."""

    def intermediate_frame_helpers_write_arrays(
        self,
        arrays: Iterable[np.ndarray] | np.ndarray,
        headers: Iterable[fits.Header] | fits.Header | None = None,
        task_tag: str | None = None,
        task: str | None = None,
        exposure_time: float | None = None,
        modstate: int | None = None,
        stokes: str | None = None,
    ) -> None:
        """Write an intermediate fits files given a list of input arrays and headers."""
        if task_tag is not None and task is not None:
            raise ValueError("Cannot specify both the raw 'task' and a formatted 'task_tag'.")
        if task_tag is None and task is None:
            raise ValueError("Must specify exactly one of raw 'task' or formatted 'task_tag'.")

        if task is not None:
            task_tag = DlnirspTag.task(task)
        tags = [DlnirspTag.intermediate(), DlnirspTag.frame(), task_tag]

        for arg, tag_func in zip(
            [exposure_time, modstate, stokes],
            [
                DlnirspTag.exposure_time,
                DlnirspTag.modstate,
                DlnirspTag.stokes,
            ],
        ):
            if arg is not None:
                tags.append(tag_func(arg))

        arrays = [arrays] if isinstance(arrays, np.ndarray) else arrays
        if headers is not None:
            headers = [headers] if isinstance(headers, fits.Header) else headers
        else:
            headers = itertools.repeat(None)

        filenames = []
        for array, header in zip(arrays, headers):
            written_name = self.write(
                data=array, header=header, encoder=fits_array_encoder, tags=tags
            )
            filenames.append(str(written_name))

        logger.info(f"Wrote intermediate file for {tags = } to {filenames}")

    def intermediate_frame_helpers_write_dark_array(
        self, arrays: Iterable[np.ndarray] | np.ndarray, exposure_time: float
    ) -> None:
        """Write intermediate dark frame."""
        self.intermediate_frame_helpers_write_arrays(
            arrays=arrays, task=TaskName.dark.value, exposure_time=exposure_time
        )

    def intermediate_frame_helpers_write_lamp_gain_array(
        self,
        arrays: Iterable[np.ndarray] | np.ndarray,
    ) -> None:
        """Write intermediate dark frame."""
        self.intermediate_frame_helpers_write_arrays(arrays=arrays, task=TaskName.lamp_gain.value)

    def intermediate_frame_helpers_write_solar_gain_array(self, array: np.ndarray) -> None:
        """Write an intermediate solar gain frame."""
        self.intermediate_frame_helpers_write_arrays(arrays=array, task=TaskName.solar_gain.value)

    ###########
    # Loaders #
    ###########
    def intermediate_frame_helpers_load_arrays(
        self, tags: list[str]
    ) -> Generator[np.ndarray, None, None]:
        """Load numpy arrays from intermediate frames given the input tags."""
        tags = list(set([DlnirspTag.intermediate(), DlnirspTag.frame()] + tags))

        if self.scratch.count_all(tags=tags) == 0:
            raise RuntimeError(f"No files found matching {tags =}")
        yield from self.read(tags=tags, decoder=fits_array_decoder)

    def intermediate_frame_helpers_load_dark_array(self, exposure_time: float) -> np.ndarray:
        """Load intermediate DARK calibration objects for a given exposure time."""
        tags = [DlnirspTag.task_dark(), DlnirspTag.exposure_time(exposure_time)]
        dark_list = list(self.intermediate_frame_helpers_load_arrays(tags=tags))
        if len(dark_list) > 1:
            logger.warning(
                f"More than 1 dark found for {exposure_time = }. Only using the first one."
            )

        return dark_list[0]

    def intermediate_frame_helpers_load_solar_gain_array(self) -> np.ndarray:
        """Load the intermediate SOLAR_GAIN calibration array."""
        tags = [DlnirspTag.task_solar_gain()]
        solar_gain_list = list(self.intermediate_frame_helpers_load_arrays(tags=tags))
        if len(solar_gain_list) > 1:
            logger.warning("More than 1 solar gain frame found. Using the first one.")

        return solar_gain_list[0]

    def intermediate_frame_helpers_load_geometric_calibration(
        self,
    ) -> tuple[dict[int, np.ndarray], dict[int, np.ndarray], np.ndarray]:
        """Load intermediate GEOMETRIC calibration object and unpack into shift and scale dictionaries."""
        tags = [DlnirspTag.intermediate(), DlnirspTag.task_geometric()]
        trees = list(self.read(tags=tags, decoder=asdf_decoder))
        if len(trees) > 1:
            logger.warning("More than one geometric correction found. This is very strange.")

        spectral_shifts = trees[0]["spectral_shifts"]
        spectral_scales = trees[0]["spectral_scales"]
        reference_wavelength_axis = trees[0]["reference_wavelength_axis"]

        return spectral_shifts, spectral_scales, reference_wavelength_axis

    def intermediate_frame_helpers_load_demodulation_array(self) -> np.ndarray:
        """Load intermediate DARK calibration objects for a given exposure time."""
        tags = [DlnirspTag.task_demodulation_matrices()]
        demod_list = list(self.intermediate_frame_helpers_load_arrays(tags=tags))

        return demod_list[0]
