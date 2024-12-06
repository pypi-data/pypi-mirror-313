"""Helper to manage input data."""
from collections.abc import Generator

import numpy as np
from astropy.io import fits
from dkist_processing_common.codecs.fits import fits_access_decoder
from dkist_processing_common.models.fits_access import FitsAccessBase
from dkist_processing_common.models.task_name import TaskName

from dkist_processing_cryonirsp.models.exposure_conditions import ExposureConditions
from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.parsers.cryonirsp_l0_fits_access import CryonirspL0FitsAccess


class LinearizedFrameMixin:
    """
    Mixin for methods that support easy loading of linearity corrected frames.

    Throughout this class wse assume that if beam is None, then it means to return the entire array.
    """

    def linearized_frame_fits_access_generator(
        self,
        tags: [str],
        beam: int,
    ) -> Generator[CryonirspL0FitsAccess, None, None]:
        """Load linearized fits frames based on given tags and extract the desired beam."""
        tags = list(set([CryonirspTag.linearized(), CryonirspTag.frame()] + tags))

        full_frame_generator = self.read(
            tags=tags,
            decoder=fits_access_decoder,
            fits_access_class=CryonirspL0FitsAccess,
        )
        for item in full_frame_generator:
            header = item.header
            flipped_data = self.linearized_frame_flip_dispersion_axis(item)
            data = self.beam_access_get_beam(array=flipped_data, beam=beam)
            hdu = fits.PrimaryHDU(header=header, data=data)
            yield CryonirspL0FitsAccess(hdu=hdu)

    def linearized_frame_full_array_generator(
        self,
        tags: [str],
    ) -> Generator[np.ndarray, None, None]:
        """Load linearized fits frames based on given tags."""
        tags = list(set([CryonirspTag.linearized(), CryonirspTag.frame()] + tags))
        frame_generator = self.read(
            tags=tags,
            decoder=fits_access_decoder,
            fits_access_class=CryonirspL0FitsAccess,
        )
        for frame in frame_generator:
            yield self.linearized_frame_flip_dispersion_axis(frame)

    def linearized_frame_dark_array_generator(
        self, exposure_conditions: ExposureConditions, beam: int
    ) -> Generator[np.ndarray, None, None]:
        """
        Return a fits access generator with dark frames for the given parameters.

        Parameters
        ----------
        exposure_conditions
            The current exposure conditions
        modstate
            The current modulator state
        beam
            The current beam number

        Returns
        -------
        A fits access generator based on the inputs provided
        """
        tags = [CryonirspTag.task_dark(), CryonirspTag.exposure_conditions(exposure_conditions)]
        dark_array_fits_access = self.linearized_frame_fits_access_generator(tags=tags, beam=beam)
        for array in dark_array_fits_access:
            yield array.data

    def linearized_frame_polcal_dark_array_generator(
        self,
        exposure_conditions: ExposureConditions,
        beam: int,
    ) -> Generator[np.ndarray, None, None]:
        """
        Return a fits access generator with polcal dark frames based on the given parameters.

        Parameters
        ----------
        beam
            The beam from which to return data
        exposure_conditions
            The current exposure conditions

        Returns
        -------
        A fits access generator based on the inputs provided
        """
        tags = [
            CryonirspTag.task_polcal_dark(),
            CryonirspTag.exposure_conditions(exposure_conditions),
        ]
        polcal_dark_array_fits_access = self.linearized_frame_fits_access_generator(
            tags=tags,
            beam=beam,
        )
        for array in polcal_dark_array_fits_access:
            yield array.data

    def linearized_frame_gain_array_generator(
        self,
        gain_type: str,
        beam: int,
        exposure_conditions: ExposureConditions | None = None,
    ) -> Generator[np.ndarray, None, None]:
        """
        Return a fits access generator with gain frames based on the parameters provided.

        Parameters
        ----------
        gain_type
            The gain type
        exposure_conditions
            The current exposure conditions
        beam
            The current beam number

        Returns
        -------
        A fits access generator based on the inputs provided
        """
        tags = [CryonirspTag.task(gain_type)]
        if exposure_conditions is not None:
            tags.append(CryonirspTag.exposure_conditions(exposure_conditions))
        gain_array_fits_access = self.linearized_frame_fits_access_generator(
            tags=tags,
            beam=beam,
        )
        for array in gain_array_fits_access:
            yield array.data

    def linearized_frame_lamp_gain_array_generator(
        self,
        beam: int,
        exposure_conditions: float | None = None,
    ) -> Generator[np.ndarray, None, None]:
        """
        Return a fits access generator with lamp gain frames based on the parameters provided.

        Parameters
        ----------
        exposure_conditions
            The current exposure conditions
        beam
            The current beam number

        Returns
        -------
        A fits access generator based on the inputs provided
        """
        return self.linearized_frame_gain_array_generator(
            gain_type=TaskName.lamp_gain.value, beam=beam, exposure_conditions=exposure_conditions
        )

    def linearized_frame_solar_gain_array_generator(
        self,
        beam: int,
        exposure_conditions: float | None = None,
    ) -> Generator[np.ndarray, None, None]:
        """
        Return a fits access generator with solar gain frames based on the parameters provided.

        Parameters
        ----------
        exposure_conditions
            The current exposure conditions
        beam
            The current beam number

        Returns
        -------
        A fits access generator based on the inputs provided
        """
        return self.linearized_frame_gain_array_generator(
            gain_type=TaskName.solar_gain.value, beam=beam, exposure_conditions=exposure_conditions
        )

    def linearized_frame_polcal_gain_array_generator(
        self,
        exposure_conditions: ExposureConditions,
        beam: int,
    ) -> Generator[np.ndarray, None, None]:
        """
        Return a fits access generator with polcal gain frames based on the given parameters.

        Parameters
        ----------
        beam
            The beam from which to return data
        exposure_conditions
            The current exposure conditions

        Returns
        -------
        A fits access generator based on the inputs provided
        """
        tags = [
            CryonirspTag.task_polcal_gain(),
            CryonirspTag.exposure_conditions(exposure_conditions),
        ]
        polcal_gain_array_fits_access = self.linearized_frame_fits_access_generator(
            tags=tags,
            beam=beam,
        )
        for array in polcal_gain_array_fits_access:
            yield array.data

    def linearized_frame_observe_fits_access_generator(
        self,
        modstate: int,
        meas_num: int,
        scan_step: int,
        map_scan: int,
        exposure_conditions: ExposureConditions,
        beam: int,
    ) -> Generator[FitsAccessBase, None, None]:
        """
        Return a fits access generator of observe frames based on the parameters provided.

        Parameters
        ----------
        beam
            The beam from which to return data
        modstate
            The current modulator state
        meas_num
            The current measurement number
        scan_step
            The current scan step
        map_scan
            The current map_scan number
        exposure_conditions
            The current exposure conditions

        Returns
        -------
        A fits access generator based on the inputs provided
        """
        tags = [
            CryonirspTag.task_observe(),
            CryonirspTag.modstate(modstate),
            CryonirspTag.meas_num(meas_num),
            CryonirspTag.scan_step(scan_step),
            CryonirspTag.map_scan(map_scan),
            CryonirspTag.exposure_conditions(exposure_conditions),
        ]
        return self.linearized_frame_fits_access_generator(
            tags=tags,
            beam=beam,
        )

    def linearized_frame_polcal_fits_access_generator(
        self,
        modstate: int,
        cs_step: int,
        exposure_conditions: ExposureConditions,
        beam: int,
    ) -> Generator[FitsAccessBase, None, None]:
        """
        Return a fits access generator of polcal frames based on the parameters provided.

        Parameters
        ----------
        modstate
            The current modulator state
        cs_step
            The current cs_step number
        exposure_conditions
            The current exposure conditions
        beam
            The current beam number

        Returns
        -------
        A fits access generator based on the inputs provided
        """
        tags = [
            CryonirspTag.task_polcal(),
            CryonirspTag.modstate(modstate),
            CryonirspTag.cs_step(cs_step),
            CryonirspTag.exposure_conditions(exposure_conditions),
        ]
        return self.linearized_frame_fits_access_generator(
            tags=tags,
            beam=beam,
        )

    @staticmethod
    def linearized_frame_flip_dispersion_axis(frame: CryonirspL0FitsAccess) -> np.ndarray:
        """
        Flip dispersion axis. Cryo's wavelength decreases from left to right, so we flip it here to match the other instruments.

        :param frame: frame to be flipped
        :return: flipped array (SP), array (CI)
        """
        if frame.arm_id == "SP":
            return np.flip(frame.data, 1)
        elif frame.arm_id == "CI":
            return frame.data
