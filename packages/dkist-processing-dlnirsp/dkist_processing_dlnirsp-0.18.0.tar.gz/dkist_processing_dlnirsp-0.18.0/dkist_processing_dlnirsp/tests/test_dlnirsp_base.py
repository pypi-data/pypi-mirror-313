import pytest

from dkist_processing_dlnirsp.models.constants import DlnirspConstants
from dkist_processing_dlnirsp.models.parameters import DlnirspParameters
from dkist_processing_dlnirsp.tasks.dlnirsp_base import DlnirspLinearityTaskBase
from dkist_processing_dlnirsp.tasks.dlnirsp_base import DlnirspTaskBase
from dkist_processing_dlnirsp.tests.conftest import DlnirspTestingConstants


@pytest.fixture()
def dummy_arm_id() -> str:
    return "ARMY_MCARMFACE"


@pytest.fixture()
def dummy_wavelength() -> float:
    return 6.28


@pytest.fixture(
    params=[
        pytest.param(DlnirspTaskBase, id="Science Base"),
        pytest.param(DlnirspLinearityTaskBase, id="Linearization Base"),
    ]
)
def dlnirsp_science_task(
    session_recipe_run_id, session_link_constants_db, request, dummy_arm_id, dummy_wavelength
):
    base_task = request.param
    wavelength = dummy_wavelength if base_task is DlnirspTaskBase else 0.0

    class Task(base_task):
        def run(self) -> None:
            pass

    session_link_constants_db(
        recipe_run_id=session_recipe_run_id,
        constants_obj=DlnirspTestingConstants(ARM_ID=dummy_arm_id, WAVELENGTH=wavelength),
    )

    with Task(
        recipe_run_id=session_recipe_run_id,
        workflow_name="dlnirsp_base_test",
        workflow_version="x.y.z",
    ) as task:
        yield task, wavelength
        task._purge()


def test_base_constants_class(dlnirsp_science_task, dummy_arm_id):
    """
    Given: A Science task made from a DL task base
    When: Instantiating the class
    Then: The task's constants object is a DlnirspConstants object
    """
    task, _ = dlnirsp_science_task

    assert type(task.constants) is DlnirspConstants
    assert task.constants.arm_id == dummy_arm_id


def test_base_parameters_class(dlnirsp_science_task, dummy_wavelength):
    """
    Given: A Science task made from a DL task base
    When: Instantiating the class
    Then: DlnirspTaskBase has a DlnirspParameters object and DlnirspLinearityTaskBase doesn't have any parameters
    """
    task, expected_wave = dlnirsp_science_task

    if isinstance(task, DlnirspTaskBase):
        assert type(task.parameters) is DlnirspParameters
        assert task.parameters._wavelength == expected_wave
    else:
        with pytest.raises(AttributeError):
            task.parameters
