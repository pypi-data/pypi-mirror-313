import re
from dataclasses import dataclass
from functools import partial

import numpy as np
import pytest
from astropy.io import fits
from astropy.time import Time
from astropy.time import TimeDelta
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.models.task_name import TaskName
from dkist_processing_common.tests.conftest import FakeGQLClient
from dkist_service_configuration.logging import logger

from dkist_processing_dlnirsp.models.tags import DlnirspTag
from dkist_processing_dlnirsp.tasks import LinearityCorrection
from dkist_processing_dlnirsp.tests.conftest import AbortedRampHeaders
from dkist_processing_dlnirsp.tests.conftest import BadNumFramesPerRampHeaders
from dkist_processing_dlnirsp.tests.conftest import DlnirspTestingConstants
from dkist_processing_dlnirsp.tests.conftest import RawRampHeaders
from dkist_processing_dlnirsp.tests.conftest import SimpleModulatedHeaders
from dkist_processing_dlnirsp.tests.conftest import write_frames_to_task


@pytest.fixture
def linearity_correction_task(recipe_run_id, tmp_path):
    with LinearityCorrection(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        task.scratch = WorkflowFileSystem(recipe_run_id=recipe_run_id, scratch_base_path=tmp_path)

        yield task

        task._purge()


def write_ramps_to_task(task, num_ramps: int, arm_id: str, num_reset: int = 4, num_coadd: int = 1):
    start_date = "2024-04-20T16:20:00.00"
    ramp_length_sec = 3.14159
    bias_value = 5.0
    num_line = 2
    num_read = 3

    start_date_obj = Time(start_date)
    time_delta = TimeDelta(ramp_length_sec, format="sec")
    expected_obs_time_list = [(start_date_obj + time_delta * i).fits for i in range(num_ramps)]

    ramp_data_func = partial(make_ramp_data, bias=bias_value)

    dataset = RawRampHeaders(
        array_shape=(1, 2, 2),
        num_ramps=num_ramps,
        num_line=num_line,
        num_read=num_read,
        num_reset=num_reset,
        num_coadd=num_coadd,
        ramp_length_sec=ramp_length_sec,
        start_date=start_date,
        arm_id=arm_id,
    )

    write_frames_to_task(
        task=task,
        frame_generator=dataset,
        data_func=ramp_data_func,
        extra_tags=[DlnirspTag.input()],
        tag_func=tag_on_time_obs,
    )

    return expected_obs_time_list, ramp_length_sec, bias_value, num_line, num_read, num_reset


def write_skipable_ramps_to_task(task):

    # Write one good frame
    good_start_date = write_ramps_to_task(task, num_ramps=1, arm_id="JBand")[0][0]

    ramp_data_func = partial(make_ramp_data, bias=1.0)

    # Write one aborted ramp
    aborted_start_date = "2024-06-28T11:55:30.230"  # Needs to be different than the start_date in `write_ramps_to_task`
    aborted_generator = AbortedRampHeaders(
        array_shape=(1, 2, 2),
        num_line=2,
        num_read=3,
        num_reset=4,
        start_date=aborted_start_date,
    )

    write_frames_to_task(
        task,
        frame_generator=aborted_generator,
        data_func=ramp_data_func,
        extra_tags=[DlnirspTag.input()],
        tag_func=tag_on_time_obs,
    )

    # Write one ramp with weird header values
    bad_ramp_start_date = "2024-03-14T15:55:30.231"  # Needs to be different than the start_date in `write_ramps_to_task`
    bad_ramp_generator = BadNumFramesPerRampHeaders(
        array_shape=(1, 2, 2),
        num_line=2,
        num_read=3,
        num_reset=4,
        start_date=bad_ramp_start_date,
    )

    write_frames_to_task(
        task,
        frame_generator=bad_ramp_generator,
        data_func=ramp_data_func,
        extra_tags=[DlnirspTag.input()],
        tag_func=tag_on_time_obs,
    )

    return good_start_date, aborted_start_date, bad_ramp_start_date


def make_ramp_data(frame: RawRampHeaders, bias: float):
    shape = frame.array_shape
    if frame.frame_in_coadd not in range(frame.num_line, frame.num_line + frame.num_read):
        value = bias

    else:
        value = (
            (frame.current_ramp + 1) * 100.0
            + (frame.frame_in_coadd + 1) * 10
            + frame.current_coadd_in_ramp
        )

    return np.ones(shape) * value


def write_vis_inputs_to_task(task, num_frames):
    dataset = SimpleModulatedHeaders(
        num_modstates=num_frames,
        array_shape=(1, 2, 2),
        task=TaskName.dark.value,
        exp_time_ms=10.0,
        arm_id="VIS",
    )

    write_frames_to_task(
        task=task,
        frame_generator=dataset,
        data_func=make_vis_data,
        extra_tags=[DlnirspTag.input()],
        tag_func=tag_on_time_obs,
    )


def make_vis_data(frame: SimpleModulatedHeaders):
    modstate = frame.header()["DLN__015"]
    return np.ones(frame.array_shape) * modstate


def tag_on_time_obs(frame: RawRampHeaders):
    time_obs = frame.header()["DATE-OBS"]
    return [DlnirspTag.time_obs(time_obs)]


@dataclass
class DummyRampFitsAccess:
    """Just a class that has the two properties that are checked during ramp validation."""

    num_frames_in_ramp: int
    camera_sample_sequence: str
    ip_task_type: str = "TASK"


@pytest.mark.parametrize("arm_id", [pytest.param("JBand"), pytest.param("HBand")])
@pytest.mark.parametrize(
    "num_reset", [pytest.param(0, id="no_resets"), pytest.param(4, id="with_resets")]
)
@pytest.mark.parametrize(
    "num_coadd", [pytest.param(1, id="1_coadd"), pytest.param(3, id="3_coadds")]
)
def test_linearity_correction(
    linearity_correction_task, link_constants_db, arm_id, mocker, num_reset, num_coadd
):
    """
    Given: A `LinearityCorrection` task and some raw INPUT frames
    When: Linearizing the data
    Then: The correct number of frames are produced and they have the expected linearized values
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    num_ramps = 3
    task = linearity_correction_task
    (
        expected_time_obs_list,
        ramp_length_sec,
        bias_value,
        num_line,
        num_read,
        num_reset,
    ) = write_ramps_to_task(
        task, num_ramps=num_ramps, arm_id=arm_id, num_reset=num_reset, num_coadd=num_coadd
    )

    link_constants_db(
        task.recipe_run_id,
        DlnirspTestingConstants(TIME_OBS_LIST=tuple(expected_time_obs_list), ARM_ID=arm_id),
    )

    task()

    expected_avg_coadd_value = float(np.mean(range(num_coadd)))
    expected_total_exp = ramp_length_sec / num_coadd * 1000
    expected_NDR_exp = ramp_length_sec / num_coadd / num_read * 1000

    assert len(list(task.read([DlnirspTag.frame(), DlnirspTag.linearized()]))) == num_ramps
    for ramp_num, time_obs in enumerate(expected_time_obs_list, start=1):
        files = list(
            task.read([DlnirspTag.frame(), DlnirspTag.linearized(), DlnirspTag.time_obs(time_obs)])
        )
        assert len(files) == 1
        # See `make_ramp_data` for where this comes from - we don't include num_reset because we only care about the last read frame
        expected_value = (
            ramp_num * 100 + (num_line + num_read) * 10 - bias_value + expected_avg_coadd_value
        )
        data = fits.getdata(files[0])
        np.testing.assert_array_equal(data, expected_value)

        header = fits.getheader(files[0])
        assert header["XPOSURE"] == expected_total_exp
        assert header["TEXPOSUR"] == expected_NDR_exp


def test_VIS_linearity_correction(linearity_correction_task, link_constants_db, mocker):
    """
    Given: A `LinearityCorrection` task and some raw visible INPUT frames
    When: Linearizing the data
    Then: The visible frames are re-tagged as LINEARIZED and their data are un-changed
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    num_frames = 3
    task = linearity_correction_task
    write_vis_inputs_to_task(task, num_frames=num_frames)

    link_constants_db(task.recipe_run_id, DlnirspTestingConstants(ARM_ID="VIS"))
    task()

    linearized_frame_list = list(task.read([DlnirspTag.frame(), DlnirspTag.linearized()]))
    assert len(linearized_frame_list) == num_frames

    # All INPUT frames should be retagged as LINEARIZED
    assert len(list(task.read([DlnirspTag.frame(), DlnirspTag.input()]))) == 0

    for path in linearized_frame_list:
        hdu = fits.open(path)[0]
        modstate = hdu.header["DLN__015"]  # See `make_vis_data`
        np.testing.assert_array_equal(hdu.data, modstate)


@pytest.mark.parametrize(
    "camera_sequence, expected_results",
    [
        pytest.param("2line,3read", [[2, 3]], id="2line,3read"),
        pytest.param("14line,3read,23line", [[14, 3]], id="14line,3read,23line"),
        pytest.param(
            "3line,34read,3line,34read", [[3, 34], [3, 34]], id="3line,34read,3line,34read"
        ),
        pytest.param(
            "1line,2read,1line,2read,45line",
            [[1, 2], [1, 2]],
            id="1line,2read,1line,2read,45line",
        ),
        pytest.param(
            "1line,2read,1line,2read,1line,2read,1line,2read",
            [[1, 2], [1, 2], [1, 2], [1, 2]],
            id="1line,2read,1line,2read,1line,2read,1line,2read",
        ),
        pytest.param(
            "3line,2read,3line,2read,3line,2read,1line",
            [[3, 2], [3, 2], [3, 2]],
            id="3line,2read,3line,2read,3line,2read,1line",
        ),
    ],
)
def test_parse_camera_sample_sequence(linearity_correction_task, camera_sequence, expected_results):
    """
    Given: A `LinearityCorrection` task and a camera sample sequence
    When: Parsing the sample sequence into line-read-line numbers per coadd
    Then: The correct results is returned
    """
    assert (
        linearity_correction_task.parse_camera_sample_sequence(camera_sequence) == expected_results
    )


def test_linearity_correction_with_invalid_ramps(
    linearity_correction_task, link_constants_db, mocker
):
    """
    Given: A `LinearityCorrection` task and raw INPUT frames that include 2 invalid ramps
    When: Linearizing the data
    Then: The invalid ramps are not linearized
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task = linearity_correction_task
    good_time, aborted_time, bad_time = write_skipable_ramps_to_task(task)
    time_obs_list = [good_time, aborted_time, bad_time]
    link_constants_db(
        task.recipe_run_id, DlnirspTestingConstants(TIME_OBS_LIST=tuple(time_obs_list))
    )

    task()

    assert len(list(task.read([DlnirspTag.frame(), DlnirspTag.linearized()]))) == 1
    assert (
        len(
            list(
                task.read(
                    [DlnirspTag.frame(), DlnirspTag.linearized(), DlnirspTag.time_obs(good_time)]
                )
            )
        )
        == 1
    )
    assert (
        len(
            list(
                task.read(
                    [DlnirspTag.frame(), DlnirspTag.linearized(), DlnirspTag.time_obs(aborted_time)]
                )
            )
        )
        == 0
    )
    assert (
        len(
            list(
                task.read(
                    [DlnirspTag.frame(), DlnirspTag.linearized(), DlnirspTag.time_obs(bad_time)]
                )
            )
        )
        == 0
    )


@pytest.mark.parametrize(
    "ramp_list, valid, message",
    [
        pytest.param(
            [
                DummyRampFitsAccess(num_frames_in_ramp=2, camera_sample_sequence=""),
                DummyRampFitsAccess(num_frames_in_ramp=3, camera_sample_sequence=""),
            ],
            False,
            "Not all frames have the same FRAMES_IN_RAMP value",
            id="bad_num_frames_set",
        ),
        pytest.param(
            [DummyRampFitsAccess(num_frames_in_ramp=4, camera_sample_sequence="")],
            False,
            "Missing some ramp frames. Expected 4 from header value",
            id="wrong_number_from_header",
        ),
        pytest.param(
            [
                DummyRampFitsAccess(num_frames_in_ramp=2, camera_sample_sequence="1line,2read"),
                DummyRampFitsAccess(num_frames_in_ramp=2, camera_sample_sequence="1line,3read"),
            ],
            False,
            "Not all frames have the same camera sample sequence",
            id="bad_sequence_set",
        ),
        pytest.param(
            [
                DummyRampFitsAccess(
                    num_frames_in_ramp=1, camera_sample_sequence="1line,2read,1line,3read,5line"
                )
            ],
            False,
            "Sample sequence is not the same for all coadds.",
            id="multi_coadd_seq",
        ),
        pytest.param(
            [
                DummyRampFitsAccess(
                    num_frames_in_ramp=2, camera_sample_sequence="1line,2read,1line,2read,4line"
                ),
                DummyRampFitsAccess(
                    num_frames_in_ramp=2, camera_sample_sequence="1line,2read,1line,2read,4line"
                ),
            ],
            False,
            "Missing some ramp frames. Expected 10 from sample sequence",
            id="wrong_number_from_seq",
        ),
        pytest.param(
            [
                DummyRampFitsAccess(
                    num_frames_in_ramp=1,
                    camera_sample_sequence="1line,2read,3line,1line,2read,3line",
                ),
            ],
            False,
            "Malformed camera sample sequence",
            id="bad_cam_seq",
        ),
        pytest.param(
            [
                DummyRampFitsAccess(num_frames_in_ramp=2, camera_sample_sequence="1line,1read"),
                DummyRampFitsAccess(num_frames_in_ramp=2, camera_sample_sequence="1line,1read"),
            ],
            True,
            "",
            id="valid",
        ),
    ],
)
def test_is_ramp_valid(linearity_correction_task, ramp_list, valid, message, caplog):
    """
    Given: A list of ramp fits access objects
    When: Testing the ramp validity with `is_ramp_valid`
    Then: The correct answer is returned
    """
    logger.add(caplog.handler)
    assert linearity_correction_task.is_ramp_valid(ramp_list) is valid
    if not valid:
        assert re.search(message, caplog.text)
