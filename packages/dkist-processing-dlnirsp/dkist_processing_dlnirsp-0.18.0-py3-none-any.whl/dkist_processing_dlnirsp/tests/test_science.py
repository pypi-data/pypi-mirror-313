import json

import numpy as np
import pytest
from astropy.io import fits
from dkist_data_simulator.spec122 import Spec122Dataset
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.codecs.fits import fits_array_encoder
from dkist_processing_common.models.task_name import TaskName
from dkist_processing_common.tests.conftest import FakeGQLClient

from dkist_processing_dlnirsp.models.tags import DlnirspTag
from dkist_processing_dlnirsp.tasks.science import CalibrationCollection
from dkist_processing_dlnirsp.tasks.science import ScienceCalibration
from dkist_processing_dlnirsp.tests.conftest import DlnirspTestingConstants
from dkist_processing_dlnirsp.tests.conftest import DlnirspTestingParameters
from dkist_processing_dlnirsp.tests.conftest import SimpleModulatedHeaders
from dkist_processing_dlnirsp.tests.conftest import tag_obs_on_mosaic_dither_modstate
from dkist_processing_dlnirsp.tests.conftest import write_dark_frames_to_task
from dkist_processing_dlnirsp.tests.conftest import write_geometric_calibration_to_task
from dkist_processing_dlnirsp.tests.conftest import write_observe_frames_to_task
from dkist_processing_dlnirsp.tests.conftest import write_simple_frames_to_task
from dkist_processing_dlnirsp.tests.conftest import write_solar_gain_frames_to_task


@pytest.fixture
def dark_signal() -> float:
    return 100.0


@pytest.fixture
def solar_signal() -> float:
    return 2000.0


@pytest.fixture
def true_stokes_science_signal() -> np.ndarray:
    return np.array([4000.0, -1000.0, 2000.0, 1000.0])


@pytest.fixture
def modulated_science_signal(true_stokes_science_signal, modulation_matrix) -> np.ndarray:
    modulated_data = modulation_matrix @ true_stokes_science_signal  # shape = (8,)
    return modulated_data


@pytest.fixture
def make_dark_data(dark_signal):
    def make_array(frame: Spec122Dataset):
        shape = frame.array_shape[1:]
        return np.ones(shape) * dark_signal

    return make_array


@pytest.fixture
def make_solar_data(solar_signal):
    def make_array(frame: Spec122Dataset):
        shape = frame.array_shape[1:]
        return np.ones(shape) * solar_signal

    return make_array


@pytest.fixture
def make_full_demodulation_matrix(demodulation_matrix):
    def make_array(frame: Spec122Dataset):
        array_shape = frame.array_shape[1:]
        return np.ones(array_shape + demodulation_matrix.shape) * demodulation_matrix

    return make_array


@pytest.fixture
def make_linearized_science_data(
    dark_signal, solar_signal, modulated_science_signal, modulation_matrix
):
    def make_array(frame: SimpleModulatedHeaders):
        shape = frame.array_shape[1:]
        modstate = frame.current_modstate("foo") - 1
        raw_data = np.ones(shape) * modulated_science_signal[modstate]
        obs_data = (raw_data * solar_signal) + dark_signal
        return obs_data

    return make_array


@pytest.fixture
def science_task_with_data(
    tmp_path,
    recipe_run_id,
    link_constants_db,
    assign_input_dataset_doc_to_task,
    constants_class_with_different_num_slits,
    is_polarimetric,
):
    science_obs_time = 1.0
    num_dither = 2
    num_modstates = 8 if is_polarimetric else 1
    num_X_tiles = 2
    num_Y_tiles = 3
    num_mosaic = 2
    pol_mode = "Full Stokes" if is_polarimetric else "Stokes I"
    constants = DlnirspTestingConstants(
        OBSERVE_EXPOSURE_TIMES=(science_obs_time,),
        NUM_MODSTATES=num_modstates,
        NUM_SPATIAL_STEPS_X=num_X_tiles,
        NUM_SPATIAL_STEPS_Y=num_Y_tiles,
        NUM_MOSAIC_REPEATS=num_mosaic,
        NUM_DITHER_STEPS=num_dither,
        POLARIMETER_MODE=pol_mode,
    )
    link_constants_db(
        recipe_run_id=recipe_run_id,
        constants_obj=constants,
    )

    with ScienceCalibration(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        parameters = DlnirspTestingParameters()
        assign_input_dataset_doc_to_task(
            task,
            parameters,
        )

        task.scratch = WorkflowFileSystem(scratch_base_path=tmp_path, recipe_run_id=recipe_run_id)
        task.constants = constants_class_with_different_num_slits(
            recipe_run_id=recipe_run_id, task_name="test"
        )

        yield task, science_obs_time, num_modstates, num_X_tiles, num_Y_tiles, num_dither, num_mosaic


@pytest.fixture
def science_task_with_no_data(recipe_run_id, link_constants_db):
    link_constants_db(
        recipe_run_id=recipe_run_id,
        constants_obj=DlnirspTestingConstants(),
    )
    with ScienceCalibration(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:

        yield task


@pytest.fixture
def dummy_slit_shape() -> tuple[int, int]:
    # (num_spatial_pos, num_wave)
    return (150, 13)


@pytest.fixture
def dummy_ifu_numpy_shape(dummy_slit_shape) -> tuple[int, int]:
    return (10, 15)


@pytest.fixture
def dummy_ifu_pos(dummy_slit_shape, dummy_ifu_numpy_shape) -> tuple[np.ndarray, np.ndarray]:
    # Because numpy axes ordering is different than "cartesian" ordering. The *_pos vectors will be passed
    # to `np.meshgrid`, which will correctly output a cartesian output, so we need them to be in the
    # cartesian order here.
    dummy_ifu_spatial_shape = dummy_ifu_numpy_shape[::-1]
    x_pos = (
        np.zeros(dummy_slit_shape, dtype=float)
        + np.arange(dummy_slit_shape[0])[:, None] // dummy_ifu_spatial_shape[1]
    )
    num_y_points = dummy_slit_shape[0] // dummy_ifu_spatial_shape[0]
    y_pos = (
        np.zeros(dummy_slit_shape, dtype=float)
        + np.tile(np.arange(num_y_points), dummy_ifu_spatial_shape[0])[:, None]
        + 100
    )

    return x_pos, y_pos


@pytest.fixture
def calibration_collection_with_ifu_remap(dummy_ifu_pos):
    x_pos, y_pos = dummy_ifu_pos
    return CalibrationCollection(
        dark_dict=dict(),
        solar_gain=np.empty(1),
        spec_shift=dict(),
        spec_scales=dict(),
        geo_corr_ifu_x_pos=x_pos,
        geo_corr_ifu_y_pos=y_pos,
        reference_wavelength_axis=np.empty(1),
        demod_matrices=None,
    )


@pytest.mark.parametrize(
    "is_polarimetric",
    [pytest.param(True, id="polarimetric"), pytest.param(False, id="spectrographic")],
)
def test_science_task_completes(
    science_task_with_data,
    is_polarimetric,
    make_dark_data,
    make_solar_data,
    shifts_and_scales,
    reference_wave_axis,
    make_full_demodulation_matrix,
    make_linearized_science_data,
    jband_ifu_x_pos_array,
    jband_ifu_y_pos_array,
    write_drifted_group_ids_to_task,
    mocker,
):
    """
    Given: A ScienceTask with all intermediate calibrations and a set of linearized OBSERVE frames
    When: Running the task
    Then: The task completes and the expected number of files are produced

    NOTE: We don't really check anything about correctness in this test. That's a GROGU thing.
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    (
        task,
        science_obs_time,
        num_modstates,
        num_X_tiles,
        num_Y_tiles,
        num_dither,
        num_mosaic,
    ) = science_task_with_data
    array_shape = jband_ifu_x_pos_array.shape

    write_drifted_group_ids_to_task(task)

    task.write(
        data=jband_ifu_x_pos_array,
        tags=[DlnirspTag.intermediate(), DlnirspTag.frame(), DlnirspTag.task_drifted_ifu_x_pos()],
        encoder=fits_array_encoder,
    )
    task.write(
        data=jband_ifu_y_pos_array,
        tags=[DlnirspTag.intermediate(), DlnirspTag.frame(), DlnirspTag.task_drifted_ifu_y_pos()],
        encoder=fits_array_encoder,
    )

    write_dark_frames_to_task(
        task,
        array_shape=array_shape,
        exp_time_ms=science_obs_time,
        tags=[
            DlnirspTag.intermediate(),
            DlnirspTag.task_dark(),
            DlnirspTag.exposure_time(science_obs_time),
        ],
        data_func=make_dark_data,
    )

    write_solar_gain_frames_to_task(
        task,
        array_shape=array_shape,
        num_modstates=1,
        tags=[
            DlnirspTag.intermediate(),
            DlnirspTag.task_solar_gain(),
        ],
        data_func=make_solar_data,
    )

    shift_dict, scale_dict, _, _ = shifts_and_scales
    write_geometric_calibration_to_task(
        task, shift_dict=shift_dict, scale_dict=scale_dict, wave_axis=reference_wave_axis
    )

    if is_polarimetric:
        write_simple_frames_to_task(
            task,
            task_type=TaskName.polcal.value,
            array_shape=array_shape,
            num_modstates=1,
            tags=[DlnirspTag.intermediate(), DlnirspTag.task_demodulation_matrices()],
            data_func=make_full_demodulation_matrix,
        )

    num_observe_frames = write_observe_frames_to_task(
        task,
        exp_time_ms=science_obs_time,
        array_shape=array_shape,
        num_modstates=num_modstates,
        num_X_tiles=num_X_tiles,
        num_Y_tiles=num_Y_tiles,
        num_mosaics=num_mosaic,
        dither_mode_on=True,
        tags=[DlnirspTag.linearized(), DlnirspTag.task_observe()],
        data_func=make_linearized_science_data,
        tag_func=tag_obs_on_mosaic_dither_modstate,
    )

    task()

    for mosaic in range(num_mosaic):
        for dither in range(num_dither):
            for X_tile in range(num_X_tiles):
                for Y_tile in range(num_Y_tiles):
                    for stokes in task.constants.stokes_params:
                        tags = [
                            DlnirspTag.calibrated(),
                            DlnirspTag.frame(),
                            DlnirspTag.mosaic_num(mosaic),
                            DlnirspTag.dither_step(dither),
                            DlnirspTag.tile_X_num(X_tile),
                            DlnirspTag.tile_Y_num(Y_tile),
                            DlnirspTag.stokes(stokes),
                        ]
                        file_list = list(task.read(tags=tags))
                        if not is_polarimetric and stokes in ["Q", "U", "V"]:
                            assert len(file_list) == 0
                        else:
                            assert len(file_list) == 1
                            assert file_list[0].exists

                            header = fits.getheader(file_list[0])
                            assert "DATE-END" in header
                            if is_polarimetric:
                                assert "POL_NOIS" in header
                                assert "POL_SENS" in header
                            else:
                                assert "POL_NOIS" not in header
                                assert "POL_SENS" not in header

    quality_files = list(task.read(tags=[DlnirspTag.quality("TASK_TYPES")]))
    assert len(quality_files) == 1
    file = quality_files[0]
    with file.open() as f:
        data = json.load(f)
        assert isinstance(data, dict)
        assert data["task_type"] == TaskName.observe.value
        assert data["total_frames"] == num_observe_frames
        assert data["frames_not_used"] == 0


def test_ifu_remapping(
    science_task_with_no_data,
    calibration_collection_with_ifu_remap,
    dummy_slit_shape,
    dummy_ifu_numpy_shape,
):
    """
    Given: A `ScienceCalibration` task and a `CalibrationCollection` containing IFU remapping information
    When: Remapping an IFU cube
    Then: The resulting cube has the correct dimensions and the wavelength values have not been changed
    """
    expected_wave_values = np.arange(dummy_slit_shape[1]) + 1
    raw_data = np.zeros(dummy_slit_shape, dtype=np.float64) + expected_wave_values[None, :]
    stokes_stack = raw_data[:, :, None]

    remapped_data = science_task_with_no_data.remap_ifu_cube(
        data=stokes_stack, calibrations=calibration_collection_with_ifu_remap
    )

    expected_shape = (dummy_slit_shape[1], *dummy_ifu_numpy_shape, 1)  # 1 from stokes axis
    assert remapped_data.shape == expected_shape
    for x_pos in range(dummy_ifu_numpy_shape[0]):
        for y_pos in range(dummy_ifu_numpy_shape[1]):
            np.testing.assert_allclose(remapped_data[:, x_pos, y_pos, 0], expected_wave_values)
