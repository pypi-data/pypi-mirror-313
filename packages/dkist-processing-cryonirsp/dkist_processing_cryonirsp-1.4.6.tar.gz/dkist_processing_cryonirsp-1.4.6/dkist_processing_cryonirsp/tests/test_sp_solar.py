import json

import numpy as np
import pytest
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.codecs.fits import fits_hdulist_encoder
from dkist_processing_common.tests.conftest import FakeGQLClient

from dkist_processing_cryonirsp.models.exposure_conditions import AllowableOpticalDensityFilterNames
from dkist_processing_cryonirsp.models.exposure_conditions import ExposureConditions
from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.tasks.sp_solar_gain import SPSolarGainCalibration
from dkist_processing_cryonirsp.tests.conftest import cryonirsp_testing_parameters_factory
from dkist_processing_cryonirsp.tests.conftest import CryonirspConstantsDb
from dkist_processing_cryonirsp.tests.conftest import generate_214_l0_fits_frame
from dkist_processing_cryonirsp.tests.header_models import CryonirspHeadersValidSPSolarGainFrames


@pytest.fixture(scope="function")
def solar_gain_calibration_task_that_completes(
    tmp_path,
    recipe_run_id,
    assign_input_dataset_doc_to_task,
    init_cryonirsp_constants_db,
    fringe_correction,
):
    number_of_modstates = 1
    # Be careful here!!! We have some files that are beam specific and others that contain both beams!!!
    number_of_beams = 2
    exposure_time = 20.0  # From CryonirspHeadersValidSolarGainFrames fixture
    exposure_conditions = ExposureConditions(
        exposure_time, AllowableOpticalDensityFilterNames.OPEN.value
    )
    intermediate_shape = (10, 10)
    dataset_shape = (1, 10, 20)
    array_shape = (1, 10, 20)
    constants_db = CryonirspConstantsDb(
        NUM_MODSTATES=number_of_modstates,
        SOLAR_GAIN_EXPOSURE_CONDITIONS_LIST=(exposure_conditions,),
        ARM_ID="SP",
    )
    init_cryonirsp_constants_db(recipe_run_id, constants_db)
    with SPSolarGainCalibration(
        recipe_run_id=recipe_run_id,
        workflow_name="sp_solar_gain_calibration",
        workflow_version="VX.Y",  # check workflow name?
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task.scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            param_class = cryonirsp_testing_parameters_factory(param_path=tmp_path)
            assign_input_dataset_doc_to_task(
                task, param_class(cryonirsp_fringe_correction_on=fringe_correction)
            )
            # Create fake bad pixel map
            task.intermediate_frame_write_arrays(
                arrays=np.zeros((10, 20)),
                task_tag=CryonirspTag.task_bad_pixel_map(),
            )
            for beam in range(1, number_of_beams + 1):
                # Create fake beam border intermediate arrays
                task.intermediate_frame_write_arrays(
                    arrays=np.array([0, 10, ((beam - 1) * 10), 10 + ((beam - 1) * 10)]),
                    task_tag=CryonirspTag.task_beam_boundaries(),
                    beam=beam,
                )

                # DarkCal object
                dark_cal = np.ones(intermediate_shape) * 3.0
                task.intermediate_frame_write_arrays(
                    arrays=dark_cal,
                    beam=beam,
                    task_tag=CryonirspTag.task_dark(),
                    exposure_conditions=exposure_conditions,
                )

                # Geo angles and spec_shifts
                task.intermediate_frame_write_arrays(
                    arrays=np.zeros(1),
                    beam=beam,
                    task_tag=CryonirspTag.task_geometric_angle(),
                )
                task.intermediate_frame_write_arrays(
                    arrays=np.zeros(intermediate_shape[0]),
                    beam=beam,
                    task_tag=CryonirspTag.task_geometric_sepectral_shifts(),
                )

                for modstate in range(1, number_of_modstates + 1):
                    # LampCal object
                    lamp_cal_ramp = np.arange(1, intermediate_shape[1] + 1) / 5
                    lamp_cal_ramp = np.flip(lamp_cal_ramp)
                    lamp_cal = np.ones(intermediate_shape) * lamp_cal_ramp[None, :]
                    lamp_cal /= np.nanmean(lamp_cal)
                    task.intermediate_frame_write_arrays(
                        arrays=lamp_cal,
                        beam=beam,
                        modstate=modstate,
                        task_tag=CryonirspTag.task_lamp_gain(),
                    )

                    # Geo offsets
                    task.intermediate_frame_write_arrays(
                        arrays=np.zeros(2),
                        beam=beam,
                        modstate=modstate,
                        task_tag=CryonirspTag.task_geometric_offset(),
                    )

                # Raw gain input images contain both beams, so are not beam specific!!!
                ds = CryonirspHeadersValidSPSolarGainFrames(
                    dataset_shape=dataset_shape,
                    array_shape=array_shape,
                    time_delta=10,
                )
                header = ds.header()
                true_gain = np.ones(intermediate_shape)
                true_solar_signal = (
                    np.arange(1, intermediate_shape[1] + 1) / 5
                )  # creates a trend from 0.2 to 2
                true_solar_single_beam = true_gain * true_solar_signal[None, :]
                true_solar_gain = np.concatenate(
                    (true_solar_single_beam, true_solar_single_beam), axis=1
                )
                raw_dark = np.concatenate((dark_cal, dark_cal), axis=1)
                raw_solar = true_solar_gain + raw_dark
                solar_hdul = generate_214_l0_fits_frame(data=raw_solar, s122_header=header)
                task.write(
                    data=solar_hdul,
                    tags=[
                        CryonirspTag.linearized(),
                        CryonirspTag.task_solar_gain(),
                        CryonirspTag.modstate(modstate),
                        CryonirspTag.frame(),
                        CryonirspTag.exposure_conditions(exposure_conditions),
                    ],
                    encoder=fits_hdulist_encoder,
                )

            yield task, true_solar_single_beam
        finally:
            task._purge()


@pytest.fixture(scope="function")
def solar_gain_calibration_task_with_no_data(tmp_path, recipe_run_id, init_cryonirsp_constants_db):
    number_of_modstates = 1
    constants_db = CryonirspConstantsDb(NUM_MODSTATES=number_of_modstates, ARM_ID="SP")
    init_cryonirsp_constants_db(recipe_run_id, constants_db)
    with SPSolarGainCalibration(
        recipe_run_id=recipe_run_id, workflow_name="geometric_calibration", workflow_version="VX.Y"
    ) as task:
        task.scratch = WorkflowFileSystem(scratch_base_path=tmp_path, recipe_run_id=recipe_run_id)

        yield task
        task._purge()


@pytest.mark.parametrize("fringe_correction", [False, True])
def test_solar_gain_task(solar_gain_calibration_task_that_completes, mocker, fringe_correction):
    """
    Given: A set of raw solar gain images and necessary intermediate calibrations
    When: Running the solargain task
    Then: The task completes and the outputs are correct
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )

    task, true_solar_single_beam = solar_gain_calibration_task_that_completes
    task()
    for beam in range(1, task.constants.num_beams + 1):
        for modstate in range(1, task.constants.num_modstates + 1):
            solar_gain = task.intermediate_frame_load_solar_gain_array(beam=beam)
            # If fringe correction is on, then just be happy we got a file...
            if task.parameters.fringe_correction_on:
                continue
            # The processed image is flipped, so we must flip the original to test
            expected = np.flip(true_solar_single_beam, axis=1)
            np.testing.assert_allclose(expected, solar_gain)
            # Test for the existence of the spectral corrected solar array
            spectral_corrected_array = task.intermediate_frame_load_intermediate_arrays(
                tags=[CryonirspTag.beam(beam), CryonirspTag.task("SPECTRAL_CORRECTED_SOLAR_ARRAY")]
            )

    quality_files = task.read(tags=[CryonirspTag.quality("TASK_TYPES")])
    for file in quality_files:
        with file.open() as f:
            data = json.load(f)
            assert isinstance(data, dict)
            assert data["total_frames"] == task.scratch.count_all(
                tags=[
                    CryonirspTag.linearized(),
                    CryonirspTag.frame(),
                    CryonirspTag.task_solar_gain(),
                ]
            )
