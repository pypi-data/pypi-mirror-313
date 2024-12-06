"""Mixin to support extracting the desired beam from an input image on-the-fly."""
from functools import cached_property

import numpy as np


class BeamAccessMixin:
    """Mixin that supports extracting the desired beam from an input image on-the-fly."""

    def beam_access_get_beam(self, array: np.ndarray, beam: int) -> np.ndarray:
        """
        Extract a single beam array from a dual-beam array.

        Parameters
        ----------
        array
            The input dual-beam array
        beam
            The desired beam to extract

        Returns
        -------
        An ndarray containing the extracted beam
        """
        boundaries = self.beam_boundaries[beam]
        spatial_min, spatial_max, spectral_min, spectral_max = boundaries

        if (
            spatial_min < 0
            or spatial_max > array.shape[0]
            or spectral_min < 0
            or spectral_max > array.shape[1]
        ):
            raise IndexError(
                f"beam_access_get_boundaries exceed array bounds: {boundaries = }, {array.shape = }."
            )

        return np.copy(array[spatial_min:spatial_max, spectral_min:spectral_max])

    @cached_property
    def beam_boundaries(self) -> dict[int, np.ndarray]:
        """
        Load the beam boundaries from their respective files and return as a boundary dict.

        Returns
        -------
        beam_boundary dict
        """
        boundaries = dict()
        for beam in range(1, self.constants.num_beams + 1):
            boundaries[beam] = self.intermediate_frame_load_beam_boundaries(beam=beam)
        return boundaries
