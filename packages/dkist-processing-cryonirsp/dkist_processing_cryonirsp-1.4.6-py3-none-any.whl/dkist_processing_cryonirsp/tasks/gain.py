"""Cryo gain task."""
from abc import abstractmethod
from typing import Callable

import numpy as np
from dkist_processing_common.models.task_name import TaskName
from dkist_processing_math.arithmetic import subtract_array_from_arrays
from dkist_processing_math.statistics import average_numpy_arrays
from dkist_service_configuration.logging import logger

from dkist_processing_cryonirsp.models.exposure_conditions import ExposureConditions
from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.tasks.cryonirsp_base import CryonirspTaskBase

__all__ = ["LampGainCalibration", "CISolarGainCalibration"]


class GainCalibrationBase(CryonirspTaskBase):
    """
    Base task class for calculation of average lamp or solar gains for CI and average lamp gains for SP.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    @property
    @abstractmethod
    def gain_type(self) -> str:
        """Return the gain type, SOLAR_GAIN or LAMP_GAIN."""
        pass

    @property
    @abstractmethod
    def exposure_conditions(self) -> [ExposureConditions]:
        """Return the exposure conditions list."""
        pass

    @property
    @abstractmethod
    def gain_array_generator(self) -> Callable:
        """Return the gain array generator to use based on the gain type."""
        pass

    @property
    @abstractmethod
    def normalize_gain_switch(self) -> bool:
        """If True then the final gain image is normalized to have a mean of 1."""
        pass

    record_provenance = True

    def run(self):
        """
        Execute the task.

        For each exposure time and beam:
            - Gather input gain and averaged dark arrays
            - Calculate average array
            - Normalize average array
            - Write average gain array
            - Record quality metrics

        Returns
        -------
        None

        """
        target_exposure_conditions = self.exposure_conditions

        logger.info(f"{target_exposure_conditions = }")
        with self.apm_task_step(
            f"Generate {self.gain_type} for {len(target_exposure_conditions)} exposure times"
        ):
            for exposure_conditions in target_exposure_conditions:
                # NB: By using num_beams = 1 for CI, this method works for both CI and SP
                for beam in range(1, self.constants.num_beams + 1):
                    apm_str = f"{beam = } and {exposure_conditions = }"
                    with self.apm_processing_step(f"Remove dark signal for {apm_str}"):
                        dark_array = self.intermediate_frame_load_dark_array(
                            beam=beam, exposure_conditions=exposure_conditions
                        )

                        avg_gain_array = self.compute_average_gain_array(
                            beam=beam, exposure_conditions=exposure_conditions
                        )

                        dark_corrected_gain_array = next(
                            subtract_array_from_arrays(avg_gain_array, dark_array)
                        )

                    with self.apm_processing_step(f"Correct bad pixels for {apm_str}"):
                        bad_pixel_map = self.intermediate_frame_load_bad_pixel_map(beam=beam)
                        bad_pixel_corrected_array = self.corrections_correct_bad_pixels(
                            dark_corrected_gain_array, bad_pixel_map
                        )

                    if self.normalize_gain_switch:
                        with self.apm_processing_step(f"Normalize final gain for {apm_str}"):
                            normalized_gain_array = self.normalize_gain(bad_pixel_corrected_array)
                    else:
                        normalized_gain_array = bad_pixel_corrected_array

                    with self.apm_writing_step(
                        f"Writing gain array for {beam = } and {exposure_conditions = }"
                    ):
                        self.intermediate_frame_write_arrays(
                            normalized_gain_array,
                            beam=beam,
                            task=self.gain_type,
                        )

        with self.apm_processing_step("Computing and logging quality metrics"):
            no_of_raw_gain_frames: int = self.scratch.count_all(
                tags=[
                    CryonirspTag.linearized(),
                    CryonirspTag.frame(),
                    CryonirspTag.task(self.gain_type),
                ],
            )

            self.quality_store_task_type_counts(
                task_type=self.gain_type, total_frames=no_of_raw_gain_frames
            )

    def compute_average_gain_array(
        self,
        beam: int,
        exposure_conditions: ExposureConditions,
    ) -> np.ndarray:
        """
        Compute average gain array for a given exposure conditions and beam.

        Parameters
        ----------
        beam : int
            The number of the beam

        exposure_conditions : float
            Exposure time

        Returns
        -------
        np.ndarray
        """
        linearized_gain_arrays = self.gain_array_generator(
            beam=beam, exposure_conditions=exposure_conditions
        )
        averaged_gain_data = average_numpy_arrays(linearized_gain_arrays)
        return averaged_gain_data

    @staticmethod
    def normalize_gain(gain_array: np.ndarray) -> np.ndarray:
        """
        Normalize gain to a mean of 1.

        Find any residual pixels that are zero valued and set them to 1.

        Parameters
        ----------
        gain_array : np.ndarray
            Dark corrected gain array

        Returns
        -------
        np.ndarray
            Normalized dark-corrected gain array

        """
        avg = np.nanmean(gain_array)
        gain_array /= avg

        return gain_array


class LampGainCalibration(GainCalibrationBase):
    """
    Task class for calculation of an average lamp gain frame for a CryoNIRSP CI or SP calibration run.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    @property
    def gain_type(self) -> str:
        """Return the gain type, SOLAR_GAIN or LAMP_GAIN."""
        return TaskName.lamp_gain.value

    @property
    def exposure_conditions(self) -> [ExposureConditions]:
        """Return the exposure conditions list."""
        return self.constants.lamp_gain_exposure_conditions_list

    @property
    def gain_array_generator(self) -> Callable:
        """Return the gain array generator to use based on the gain type."""
        return self.linearized_frame_lamp_gain_array_generator

    @property
    def normalize_gain_switch(self) -> True:
        """Lamp gains should be normalized."""
        return True


class CISolarGainCalibration(GainCalibrationBase):
    """
    Task class for calculation of an average solar gain frame for a CryoNIRSP CI calibration run.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    @property
    def gain_type(self) -> str:
        """Return the gain type, SOLAR_GAIN or LAMP_GAIN."""
        return TaskName.solar_gain.value

    @property
    def exposure_conditions(self) -> [ExposureConditions]:
        """Return the exposure conditions list."""
        return self.constants.solar_gain_exposure_conditions_list

    @property
    def gain_array_generator(self) -> Callable:
        """Return the gain array generator to use based on the gain type."""
        return self.linearized_frame_solar_gain_array_generator

    @property
    def normalize_gain_switch(self) -> False:
        """We don't want to normalize and Solar Gain images."""
        return False
