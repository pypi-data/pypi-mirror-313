"""Pickybud to check for lamp gain and solar gain frames."""
from typing import Hashable
from typing import Type

from dkist_processing_common.models.flower_pot import SpilledDirt
from dkist_processing_common.models.flower_pot import Stem
from dkist_processing_common.models.flower_pot import Thorn
from dkist_processing_common.models.task_name import TaskName
from dkist_processing_common.parsers.task import parse_header_ip_task_with_gains

from dkist_processing_cryonirsp.models.constants import CryonirspBudName
from dkist_processing_cryonirsp.parsers.cryonirsp_l0_fits_access import CryonirspL0FitsAccess


class CheckGainFramesPickyBud(Stem):
    """Pickybud to check for lamp gain and solar gain frames."""

    def __init__(self):
        super().__init__(stem_name=CryonirspBudName.gain_frame_type_list.value)

    def setter(self, fits_obj: CryonirspL0FitsAccess) -> Type[SpilledDirt] | str:
        """
        Set the calibration frame type for this fits object.

        Parameters
        ----------
        fits_obj
            The input fits object
        Returns
        -------
        The calibration frame object associated with this fits object
        """
        task = parse_header_ip_task_with_gains(fits_obj).casefold()

        if task in [TaskName.lamp_gain.value.casefold(), TaskName.solar_gain.value.casefold()]:
            return task
        return SpilledDirt

    def getter(self, key: Hashable) -> Thorn:
        """
        Check that lamp and solar gain frames exist. If they do, return a Thorn.

        Parameters
        ----------
        key
            The input key

        Returns
        -------
        Thorn
        """
        gain_task_types = list(self.key_to_petal_dict.values())

        if TaskName.lamp_gain.value.casefold() not in gain_task_types:
            raise ValueError("Lamp gain frames not found.")
        if TaskName.solar_gain.value.casefold() not in gain_task_types:
            raise ValueError("Solar gain frames not found.")
        return Thorn
