"""Base task for all DLNIRSP science tasks."""
from abc import ABC

from dkist_processing_common.tasks import WorkflowTaskBase
from dkist_processing_common.tasks.mixin.input_dataset import InputDatasetMixin

from dkist_processing_dlnirsp.models.constants import DlnirspConstants
from dkist_processing_dlnirsp.models.parameters import DlnirspParameters
from dkist_processing_dlnirsp.tasks.mixin.group_id import GroupIdMixin
from dkist_processing_dlnirsp.tasks.mixin.intermediate_frame_helpers import (
    IntermediateFrameHelpersMixin,
)
from dkist_processing_dlnirsp.tasks.mixin.linearized_frame_loaders import (
    LinearizedFrameLoadersMixin,
)


class DlnirspLinearityTaskBase(WorkflowTaskBase, InputDatasetMixin, ABC):
    """
    Task class for base DLNIRSP Linearization tasks.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs
    """

    # So tab completion shows all the DLNirsp constants
    constants: DlnirspConstants

    @property
    def constants_model_class(self):
        """Get DLNIRSP pipeline constants."""
        return DlnirspConstants

    def __init__(
        self,
        recipe_run_id: int,
        workflow_name: str,
        workflow_version: str,
    ):
        super().__init__(
            recipe_run_id=recipe_run_id,
            workflow_name=workflow_name,
            workflow_version=workflow_version,
        )
        # Intentionally don't set any parameters because we don't need them for linearization


class DlnirspTaskBase(
    WorkflowTaskBase,
    InputDatasetMixin,
    GroupIdMixin,
    LinearizedFrameLoadersMixin,
    IntermediateFrameHelpersMixin,
    ABC,
):
    """
    Task class for base DLNIRSP tasks.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs
    """

    # So tab completion shows all the DLNirsp constants
    constants: DlnirspConstants

    @property
    def constants_model_class(self):
        """Get DLNIRSP pipeline constants."""
        return DlnirspConstants

    def __init__(
        self,
        recipe_run_id: int,
        workflow_name: str,
        workflow_version: str,
    ):
        super().__init__(
            recipe_run_id=recipe_run_id,
            workflow_name=workflow_name,
            workflow_version=workflow_version,
        )
        self.parameters = DlnirspParameters(
            self.input_dataset_parameters,
            obs_ip_start_time=self.constants.obs_ip_start_time,
            wavelength=self.constants.wavelength,
            arm_id=self.constants.arm_id,
        )
