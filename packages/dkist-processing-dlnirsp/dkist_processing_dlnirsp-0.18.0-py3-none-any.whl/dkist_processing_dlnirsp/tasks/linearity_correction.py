"""Task to linearize raw input data. See :doc:`this page </linearization>` for more information."""
import re

import numpy as np
from astropy.io import fits
from dkist_processing_common.codecs.fits import fits_hdulist_encoder
from dkist_service_configuration.logging import logger

from dkist_processing_dlnirsp.models.tags import DlnirspTag
from dkist_processing_dlnirsp.parsers.dlnirsp_l0_fits_access import DlnirspRampFitsAccess
from dkist_processing_dlnirsp.tasks.dlnirsp_base import DlnirspLinearityTaskBase
from dkist_processing_dlnirsp.tasks.mixin.input_frame_loaders import InputFrameLoadersMixin

__all__ = ["LinearityCorrection"]


class LinearityCorrection(DlnirspLinearityTaskBase, InputFrameLoadersMixin):
    """Task class for performing linearity correction on all input frames, regardless of task type."""

    record_provenance = True

    camera_sequence_regex: re.Pattern = re.compile(r"(\d*)line,(\d*)read")
    """
    regex pattern used to parse line-read-line values for a single coadd.

    This is where we decide that camera sequences are one or more coadd sequences, where each coadd sequence is
    "Xline,Yread". The total sequence may be padded with ",Zline" reset frames, which are not captured by this regex.
    """

    def run(self):
        """
        Run method for this task.

        Steps to be performed:
            - Gather all input frames
            - Iterate through frames
                - Perform linearity correction for this frame (algorithm is TBD)
                - Get list of all tags for this frame
                - Remove input tag and add linearity_corrected tag
                - Write linearity corrected frame with updated tag list
                - Delete original frame

        Returns
        -------
        None
        """
        if self.constants.is_ir_data:
            with self.apm_task_step("Linearizing input IR frames"):
                self.linearize_IR_data()
                return

        with self.apm_task_step("Tagging non-IR frames as LINEARIZED"):
            self.tag_VIS_data_as_linearized()

    def tag_VIS_data_as_linearized(self):
        """Tag all INPUT frames as LINEARIZED."""
        for path in self.read(tags=[DlnirspTag.frame(), DlnirspTag.input()]):
            self.remove_tags(path, DlnirspTag.input())
            self.tag(path, tags=DlnirspTag.linearized())

    def linearize_IR_data(self):
        """
        Linearize data from IR cameras.

        Steps to be performed:
            - Gather all input frames
            - Iterate through frames
                - Perform linearity correction for this frame (algorithm is TBD)
                - Get list of all tags for this frame
                - Remove input tag and add linearity_corrected tag
                - Write linearity corrected frame with updated tag list
        """
        num_frames = len(self.constants.time_obs_list)
        for frame_num, time_obs in enumerate(self.constants.time_obs_list, start=1):
            logger.info(f"Processing frames from {time_obs} ({frame_num}/{num_frames})")
            input_objects = list(self.input_frame_loaders_fits_access_generator(time_obs=time_obs))

            if not self.is_ramp_valid(input_objects):
                continue

            lin_obj = self.perform_linearity_correction(input_objects)
            self.write_and_tag_linearized_frame(lin_obj, time_obs)
        logger.info(f"Processed {frame_num} frames")

    def is_ramp_valid(self, ramp_object_list: list[DlnirspRampFitsAccess]) -> bool:
        r"""
        Check if a given ramp is valid.

        Current validity checks are:

          1. All frames in the ramp have the same value for NUM_FRAMES_IN_RAMP
          2. The value of NUM_FRAMES_IN_RAMP equals the length of actual frames found
          3. All frames in the ramp have the same value for CAMERA_SAMPLE_SEQUENCE
          4. The camera sample sequence has the expected form ('(,?\d*line,\d*read)*(,\d*line)?')
          5. All coadds in the ramp have the same camera sample sequence
          6. The ramp length is equal to the expected length from the camera sample sequence

        If a ramp is not valid then the reason is logged and `False` is returned.
        """
        frames_in_ramp_set = {o.num_frames_in_ramp for o in ramp_object_list}
        task_type = ramp_object_list[0].ip_task_type

        if len(frames_in_ramp_set) > 1:
            logger.info(
                f"Not all frames have the same FRAMES_IN_RAMP value. Set is {frames_in_ramp_set}. "
                f"Ramp is task {task_type}. Skipping ramp."
            )
            return False

        num_frames_in_ramp = frames_in_ramp_set.pop()
        num_ramp_objects = len(ramp_object_list)
        if num_ramp_objects != num_frames_in_ramp:
            logger.info(
                f"Missing some ramp frames. Expected {num_frames_in_ramp} from header value, but only "
                f"have {num_ramp_objects}. Ramp is task {task_type}. Skipping ramp."
            )
            return False

        camera_sample_sequence_set = {o.camera_sample_sequence for o in ramp_object_list}
        if len(camera_sample_sequence_set) > 1:
            logger.info(
                f"Not all frames have the same camera sample sequence. Set is {camera_sample_sequence_set}. "
                f"Ramp is task {task_type}. Skipping ramp."
            )
            return False

        camera_sample_sequence = camera_sample_sequence_set.pop()
        if re.search(r"\d*line,\d*line", camera_sample_sequence):
            logger.info(
                f"Malformed camera sample sequence: '{camera_sample_sequence}'. "
                f"Ramp is task {task_type}. Skipping ramp."
            )
            return False

        coadd_sequence_nums_list = self.parse_camera_sample_sequence(camera_sample_sequence)
        if not all([s == coadd_sequence_nums_list[0] for s in coadd_sequence_nums_list]):
            logger.info(
                f"Sample sequence is not the same for all coadds. "
                f"Sequence is {camera_sample_sequence} => {coadd_sequence_nums_list}. "
                f"Ramp is task {task_type}. Skipping ramp."
            )
            return False

        num_frames_in_sample_sequence = sum(
            [int(i) for i in re.findall(r"(\d+)", camera_sample_sequence)]
        )
        if num_frames_in_sample_sequence != num_ramp_objects:
            logger.info(
                f"Missing some ramp frames. Expected {num_frames_in_sample_sequence} from sample sequence "
                f"('{camera_sample_sequence}'), but found {num_ramp_objects}. Ramp is task {task_type}. Skipping ramp."
            )
            return False

        return True

    def perform_linearity_correction(
        self, input_objects: list[DlnirspRampFitsAccess]
    ) -> fits.PrimaryHDU:
        """
        Create a linearity corrected fits object from a series of input frames (ramp).

        Parameters
        ----------
        time_obs
            The common timestamp for all frames in the series (ramp)

        Returns
        -------
        None

        """
        # Now sort them based on frame in ramp
        sorted_input_objects = sorted(input_objects, key=lambda x: x.current_frame_in_ramp)
        output_array, header = self.linearize_single_ramp(sorted_input_objects)

        hdu = fits.PrimaryHDU(data=output_array, header=header)

        return hdu

    def linearize_single_ramp(
        self, ramp_obj_list: list[DlnirspRampFitsAccess]
    ) -> tuple[np.ndarray, fits.Header]:
        """Convert a group of exposures from the same ramp into a single, linearized array.

        Steps to be performed:
             - Split "CAM_SAMPLE_SEQUENCE" for ramp into line-read indices
             - Identify coadds
             - For each coadd:
                 * Take average of data for initial line frames if more than one
                 * Subtract average initial line values from last read frame
             - Average all coadds together

        The header of the linearized frame is taken from the last "read" frame.
        """
        coadd_sequence_nums_list = self.parse_camera_sample_sequence(
            ramp_obj_list[0].camera_sample_sequence
        )
        num_coadds = len(coadd_sequence_nums_list)

        line_read_line_indices = coadd_sequence_nums_list[0]
        num_bias, num_read = line_read_line_indices[:2]

        ndr_per_coadd = num_bias + num_read

        coadd_stack = np.zeros((num_coadds, *ramp_obj_list[0].data.shape))

        for coadd in range(num_coadds):
            coadd_stack[coadd] = self.linearize_coadd(
                ramp_obj_list=ramp_obj_list,
                current_coadd=coadd,
                num_bias=num_bias,
                num_read=num_read,
                ndr_per_coadd=ndr_per_coadd,
            )

        linearized_array = np.nanmean(coadd_stack, axis=0)

        last_read_idx = (num_bias + num_read) * num_coadds - 1
        last_read_header = ramp_obj_list[last_read_idx].header

        return linearized_array, last_read_header

    def parse_camera_sample_sequence(self, camera_sample_sequence: str) -> list[list[int]]:
        """
        Identify and parse coadd sequences in the camera sample sequence.

        Reset "line" frames padding out the end of a sequence are ignored.

        Two examples of outputs given an input camera sample sequence

        "2line,3read"
            `[[2, 3]]`

        "3line,45read,3line,45read,2line"
            `[[3, 45], [3, 45]]`

        Returns
        -------
        A list of lists. Top-level list contains an item for each coadd. These items are themselves lists of
        length 2. The numbers in these inner lists correspond to the number of bias/read frames in that coadd,
        respectively.
        """
        coadd_matches = self.camera_sequence_regex.findall(camera_sample_sequence)
        coadd_sequence_numbers = [
            [int(num) for num in coadd_match] for coadd_match in coadd_matches
        ]

        return coadd_sequence_numbers

    @staticmethod
    def linearize_coadd(
        ramp_obj_list: list[DlnirspRampFitsAccess],
        *,
        current_coadd: int,
        num_bias: int,
        num_read: int,
        ndr_per_coadd: int,
    ) -> np.ndarray:
        """
        Compute a single, linearized array from a single coadd.

        This is where the actual linearization algorithm is defined.
        """
        coadd_start_idx = current_coadd * ndr_per_coadd

        running_bias_sum = np.zeros(ramp_obj_list[0].data.shape)
        for bias_line_index in range(coadd_start_idx, coadd_start_idx + num_bias):
            running_bias_sum += ramp_obj_list[bias_line_index].data

        bias_avg = running_bias_sum / num_bias

        # This does the last read frame minus the average of the initial bias frames
        # Need to cast as float because raw are uint16 and will thus explode for values below 0
        last_read_frame = ramp_obj_list[coadd_start_idx + num_bias + num_read - 1].data.astype(
            float
        )

        return last_read_frame - bias_avg

    def write_and_tag_linearized_frame(self, hdu: fits.PrimaryHDU, time_obs: str) -> None:
        """Write a linearized HDU and tag with LINEARIZED and FRAME."""
        hdu_list = fits.HDUList([hdu])

        tags = [DlnirspTag.linearized(), DlnirspTag.frame(), DlnirspTag.time_obs(time_obs)]
        self.write(data=hdu_list, tags=tags, encoder=fits_hdulist_encoder)
