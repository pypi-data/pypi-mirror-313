"""CryoNIRSP base class."""
from abc import ABC

from dkist_processing_common.tasks import WorkflowTaskBase
from dkist_processing_common.tasks.mixin.input_dataset import InputDatasetMixin
from dkist_processing_common.tasks.mixin.quality import QualityMixin

from dkist_processing_cryonirsp.models.constants import CryonirspConstants
from dkist_processing_cryonirsp.models.parameters import CryonirspParameters
from dkist_processing_cryonirsp.tasks.mixin.beam_access import BeamAccessMixin
from dkist_processing_cryonirsp.tasks.mixin.corrections import CorrectionsMixin
from dkist_processing_cryonirsp.tasks.mixin.intermediate_frame import (
    IntermediateFrameMixin,
)
from dkist_processing_cryonirsp.tasks.mixin.linearized_frame import (
    LinearizedFrameMixin,
)


class CryonirspTaskBase(
    WorkflowTaskBase,
    InputDatasetMixin,
    BeamAccessMixin,
    LinearizedFrameMixin,
    IntermediateFrameMixin,
    CorrectionsMixin,
    QualityMixin,
    ABC,
):
    """
    Task class for base CryoNIRSP tasks that occur after linearization.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs
    """

    # So tab completion shows all the Cryonirsp constants
    constants: CryonirspConstants

    @property
    def constants_model_class(self):
        """Get CryoNIRSP pipeline constants."""
        return CryonirspConstants

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
        self.parameters = CryonirspParameters(
            self.input_dataset_parameters,
            obs_ip_start_time=self.constants.obs_ip_start_time,
            wavelength=self.constants.wavelength,
            arm_id=self.constants.arm_id,
        )
