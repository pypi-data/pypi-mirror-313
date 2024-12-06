"""Buds to parse the combination of exposure time and filter name."""
from collections import namedtuple
from typing import Hashable
from typing import Type

from dkist_processing_common.models.flower_pot import SpilledDirt
from dkist_processing_common.models.flower_pot import Stem
from dkist_processing_common.models.flower_pot import Thorn
from dkist_processing_common.models.task_name import TaskName
from dkist_processing_common.parsers.task import parse_header_ip_task_with_gains

from dkist_processing_cryonirsp.models.constants import CryonirspBudName
from dkist_processing_cryonirsp.models.exposure_conditions import ExposureConditions
from dkist_processing_cryonirsp.parsers.cryonirsp_l0_fits_access import CryonirspL0FitsAccess

_DARK_AND_POLCAL_TASK_TYPES = (TaskName.dark.value, TaskName.polcal.value)


class CryonirspTaskExposureConditionsBud(Stem):
    """
    Bud to allow custom parsing of exposure conditions based on ip task type.

    Parameters
    ----------
    stem_name : str
        The name of the stem of the tag
    ip_task_type : str
        Instrument program task type
    """

    def __init__(self, stem_name: str, ip_task_type: str):
        super().__init__(stem_name=stem_name)
        self.metadata_key = "exposure_conditions"
        self.ip_task_type = ip_task_type

    def setter(self, fits_obj: CryonirspL0FitsAccess):
        """
        Set the value of the bud.

        Parameters
        ----------
        fits_obj:
            A single FitsAccess object
        """
        ip_task_type = parse_header_ip_task_with_gains(fits_obj)
        if ip_task_type.lower() == self.ip_task_type.lower():
            return getattr(fits_obj, self.metadata_key)
        return SpilledDirt

    def getter(self, key: Hashable) -> tuple[ExposureConditions, ...]:
        """Return a list of the ExposureConditions for this ip task type."""
        exposure_conditions_tuple = tuple(sorted(set(self.key_to_petal_dict.values())))
        return exposure_conditions_tuple


class CryonirspNonDarkAndNonPolcalTaskExposureConditionsBud(Stem):
    """For ip task types that are neither DARK nor POLCAL, produce a list of exposure conditions tuples."""

    def __init__(self):
        super().__init__(
            stem_name=CryonirspBudName.non_dark_and_non_polcal_task_exposure_conditions_list.value
        )
        self.metadata_key = "exposure_conditions"

    def setter(self, fits_obj: CryonirspL0FitsAccess) -> ExposureConditions | Type[SpilledDirt]:
        """
        Set the task exposure conditions tuple for this fits object.

        Parameters
        ----------
        fits_obj
            The input fits object
        Returns
        -------
        The exposure time associated with this fits object
        """
        if fits_obj.ip_task_type.upper() not in _DARK_AND_POLCAL_TASK_TYPES:
            return getattr(fits_obj, self.metadata_key)
        return SpilledDirt

    def getter(self, key: Hashable) -> tuple[ExposureConditions, ...]:
        """
        Get the list of exposure conditions tuples.

        Parameters
        ----------
        key
            The input key

        Returns
        -------
        A tuple of (exposure time, filter name) tuples
        """
        exposure_conditions_tuple = tuple(sorted(set(self.key_to_petal_dict.values())))
        return exposure_conditions_tuple


class CryonirspPickyDarkExposureConditionsBud(Stem):
    """Parse exposure conditions tuples to ensure existence of dark frames with the required exposure conditions."""

    DarkTaskTestAndExposureConditions = namedtuple(
        "DarkTaskTestAndExposureConditions", ["is_dark", "exposure_conditions"]
    )

    def __init__(self):
        super().__init__(stem_name=CryonirspBudName.picky_dark_exposure_conditions_list.value)
        self.metadata_key = "exposure_conditions"

    def setter(self, fits_obj: CryonirspL0FitsAccess) -> tuple | Type[SpilledDirt]:
        """
        Set the task exposure conditions tuple and whether it is a DARK task for this fits object.

        Parameters
        ----------
        fits_obj
            The input fits object
        Returns
        -------
        A tuple of a boolean indicating if the task is a dark task, and the exposure conditions for this fits object
        """
        if fits_obj.ip_task_type.upper() == TaskName.dark.value:
            return self.DarkTaskTestAndExposureConditions(
                is_dark=True, exposure_conditions=getattr(fits_obj, self.metadata_key)
            )
        if fits_obj.ip_task_type.upper() not in _DARK_AND_POLCAL_TASK_TYPES:
            return self.DarkTaskTestAndExposureConditions(
                is_dark=False, exposure_conditions=getattr(fits_obj, self.metadata_key)
            )
            # Polcal falls through
        return SpilledDirt

    def getter(self, key: Hashable) -> Type[Thorn]:
        """
        Parse all exposure conditions and raise an error if any non-dark exposure condition is missing from the set of dark exposure conditions.

        Parameters
        ----------
        key
            The input key

        Returns
        -------
        Thorn
        """
        dark_task_test_and_exposure_conditions_set = set(self.key_to_petal_dict.values())
        dark_exposure_conditions_set = {
            item.exposure_conditions
            for item in dark_task_test_and_exposure_conditions_set
            if item.is_dark
        }
        other_exposure_conditions_set = {
            item.exposure_conditions
            for item in dark_task_test_and_exposure_conditions_set
            if not item.is_dark
        }
        other_exposure_conditions_missing_from_dark_exposure_conditions = (
            other_exposure_conditions_set - dark_exposure_conditions_set
        )
        if other_exposure_conditions_missing_from_dark_exposure_conditions:
            raise ValueError(
                f"Exposure conditions required in the set of dark frames not found. Missing conditions = {other_exposure_conditions_missing_from_dark_exposure_conditions}"
            )
        return Thorn
