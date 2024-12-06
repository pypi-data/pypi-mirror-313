"""Mixin class providing support for loading and writing intermediate arrays."""
from collections.abc import Generator
from collections.abc import Iterable

import numpy as np
from astropy.io import fits
from dkist_processing_common.codecs.fits import fits_hdu_decoder
from dkist_processing_common.codecs.fits import fits_hdulist_encoder
from dkist_service_configuration.logging import logger

from dkist_processing_cryonirsp.models.exposure_conditions import ExposureConditions
from dkist_processing_cryonirsp.models.tags import CryonirspTag


class IntermediateFrameMixin:
    """Mixin for methods that support easy loading and writing of intermediate frames."""

    def intermediate_frame_load_intermediate_arrays(
        self,
        tags: [str],
    ) -> Generator[np.ndarray, None, None]:
        """Yield a generator that produces ndarrays for the requested tags."""
        tags = list(set([CryonirspTag.intermediate(), CryonirspTag.frame()] + tags))

        if self.scratch.count_all(tags=tags) == 0:
            raise RuntimeError(f"No files found matching {tags =}")
        for hdu in self.read(
            tags=tags,
            decoder=fits_hdu_decoder,
        ):
            yield hdu.data

    def intermediate_frame_load_beam_boundaries(self, beam: int) -> np.ndarray:
        """Return array containing beam boundaries for a given beam."""
        tags = [CryonirspTag.task_beam_boundaries(), CryonirspTag.beam(beam)]
        return next(self.intermediate_frame_load_intermediate_arrays(tags=tags))

    def intermediate_frame_load_full_bad_pixel_map(self) -> np.ndarray:
        """Return the full array version of the bad-pixel map."""
        tags = [CryonirspTag.task_bad_pixel_map()]
        bad_pixel_map = next(self.intermediate_frame_load_intermediate_arrays(tags=tags))
        return bad_pixel_map

    def intermediate_frame_load_bad_pixel_map(self, beam: int) -> np.ndarray:
        """Return bad-pixel map for given beam."""
        bad_pixel_map = self.intermediate_frame_load_full_bad_pixel_map()
        return self.beam_access_get_beam(bad_pixel_map, beam)

    def intermediate_frame_load_dark_array(
        self,
        exposure_conditions: ExposureConditions,
        beam: int,
    ) -> np.ndarray:
        """Load an existing dark array."""
        tags = [
            CryonirspTag.task_dark(),
            CryonirspTag.exposure_conditions(exposure_conditions),
            CryonirspTag.beam(beam),
        ]
        return next(self.intermediate_frame_load_intermediate_arrays(tags=tags))

    def intermediate_frame_load_polcal_dark_array(
        self,
        beam: int,
        exposure_conditions: ExposureConditions,
    ) -> np.ndarray:
        """Load an existing polcal dark array."""
        tags = [
            CryonirspTag.task_polcal_dark(),
            CryonirspTag.exposure_conditions(exposure_conditions),
            CryonirspTag.beam(beam),
        ]
        return next(self.intermediate_frame_load_intermediate_arrays(tags=tags))

    def intermediate_frame_load_solar_gain_array(self, beam: int) -> np.ndarray:
        """Load an existing solar gain array."""
        tags = [CryonirspTag.task_solar_gain(), CryonirspTag.beam(beam)]
        return next(self.intermediate_frame_load_intermediate_arrays(tags=tags))

    def intermediate_frame_load_lamp_gain_array(self, beam: int) -> np.ndarray:
        """Load an existing lamp gain array."""
        tags = [CryonirspTag.task_lamp_gain(), CryonirspTag.beam(beam)]
        return next(self.intermediate_frame_load_intermediate_arrays(tags=tags))

    def intermediate_frame_load_polcal_gain_array(
        self,
        beam: int,
        exposure_conditions: ExposureConditions,
    ) -> np.ndarray:
        """Load an existing polcal gain array."""
        tags = [
            CryonirspTag.task_polcal_gain(),
            CryonirspTag.exposure_conditions(exposure_conditions),
            CryonirspTag.beam(beam),
        ]
        return next(self.intermediate_frame_load_intermediate_arrays(tags=tags))

    def intermediate_frame_load_demod_matrices(
        self,
        beam: int,
    ) -> np.ndarray:
        """Load existing demodulation matrices."""
        tags = [CryonirspTag.task_demodulation_matrices(), CryonirspTag.beam(beam)]
        return next(self.intermediate_frame_load_intermediate_arrays(tags=tags))

    def intermediate_frame_load_angle(self, beam: int) -> float:
        """Return the geometric correction angle for a given beam."""
        tags = [CryonirspTag.task_geometric_angle(), CryonirspTag.beam(beam)]
        angle_array = next(self.intermediate_frame_load_intermediate_arrays(tags=tags))
        return float(angle_array[0])

    def intermediate_frame_load_state_offset(
        self,
        beam: int,
    ) -> np.ndarray:
        """Return state offset shifts for a given beam."""
        tags = [CryonirspTag.task_geometric_offset(), CryonirspTag.beam(beam)]
        offset = next(self.intermediate_frame_load_intermediate_arrays(tags=tags))
        return offset

    def intermediate_frame_load_spec_shift(self, beam: int) -> np.ndarray:
        """Return spectral shifts for a given beam."""
        tags = [CryonirspTag.task_geometric_sepectral_shifts(), CryonirspTag.beam(beam)]
        shifts = next(self.intermediate_frame_load_intermediate_arrays(tags=tags))
        return shifts

    def intermediate_frame_write_arrays(
        self,
        arrays: Iterable[np.ndarray] | np.ndarray,
        task_tag: str | None = None,
        task: str | None = None,
        headers: Iterable[fits.Header] | fits.Header | None = None,
        beam: int | None = None,
        modstate: int | None = None,
        map_scan: int | None = None,
        scan_step: int | None = None,
        exposure_time: float | None = None,
        exposure_conditions: ExposureConditions | None = None,
        meas_num: int | None = None,
        cs_step: int | None = None,
    ) -> None:
        """Write an intermediate fits files given a list of input arrays and headers."""
        if task_tag is not None and task is not None:
            raise ValueError("Cannot specify both the raw 'task' and a formatted 'task_tag'.")
        if task_tag is None and task is None:
            raise ValueError("Must specify exactly one of raw 'task' or formatted 'task_tag'.")

        if task is not None:
            task_tag = CryonirspTag.task(task)
        tags = [CryonirspTag.intermediate(), CryonirspTag.frame(), task_tag]
        for arg, tag_func in zip(
            [
                beam,
                modstate,
                map_scan,
                scan_step,
                exposure_time,
                meas_num,
                cs_step,
                exposure_conditions,
            ],
            [
                CryonirspTag.beam,
                CryonirspTag.modstate,
                CryonirspTag.map_scan,
                CryonirspTag.scan_step,
                CryonirspTag.exposure_time,
                CryonirspTag.meas_num,
                CryonirspTag.cs_step,
                CryonirspTag.exposure_conditions,
            ],
        ):
            if arg is not None:
                tags.append(tag_func(arg))

        arrays = [arrays] if isinstance(arrays, np.ndarray) else arrays
        if headers is not None:
            headers = [headers] if isinstance(headers, fits.Header) else headers
        else:
            headers = [None] * len(list(arrays))

        filenames = []
        for array, header in zip(arrays, headers):
            hdul = fits.HDUList([fits.PrimaryHDU(data=array, header=header)])
            path = str(
                self.write(
                    data=hdul,
                    tags=tags,
                    encoder=fits_hdulist_encoder,
                )
            )
            filenames.append(path)
        logger.info(f"Wrote intermediate file(s) for {tags = } to {filenames}")
