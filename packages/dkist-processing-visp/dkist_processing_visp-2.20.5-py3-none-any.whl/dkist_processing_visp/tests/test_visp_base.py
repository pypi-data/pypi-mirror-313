import numpy as np
import pytest
from astropy.io import fits
from dkist_processing_common.codecs.fits import fits_array_encoder
from dkist_processing_common.codecs.fits import fits_hdu_decoder

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.tasks.mixin.intermediate_frame_helpers import (
    IntermediateFrameHelpersMixin,
)
from dkist_processing_visp.tasks.visp_base import VispTaskBase
from dkist_processing_visp.tests.conftest import VispConstantsDb
from dkist_processing_visp.tests.conftest import VispInputDatasetParameterValues

NUM_BEAMS = 2
NUM_MODSTATES = 8
NUM_CS_STEPS = 6
NUM_RASTER_STEPS = 10
WAVE = 666.0


@pytest.fixture(scope="function")
def visp_science_task(recipe_run_id, assign_input_dataset_doc_to_task, init_visp_constants_db):
    class Task(VispTaskBase, IntermediateFrameHelpersMixin):
        def run(self):
            ...

    constants_db = VispConstantsDb(
        NUM_MODSTATES=NUM_MODSTATES,
        NUM_CS_STEPS=NUM_CS_STEPS,
        NUM_RASTER_STEPS=NUM_RASTER_STEPS,
        WAVELENGTH=WAVE,
        POLARIMETER_MODE="observe_polarimetric",
    )
    init_visp_constants_db(recipe_run_id, constants_db)
    with Task(
        recipe_run_id=recipe_run_id,
        workflow_name="parse_visp_input_data",
        workflow_version="VX.Y",
    ) as task:
        assign_input_dataset_doc_to_task(task, VispInputDatasetParameterValues())

        yield task

        task._purge()


def test_write_intermediate_arrays(visp_science_task):
    """
    Given: A VispTaskBase task
    When: Using the helper to write a single intermediate array
    Then: The array is written and tagged correctly
    """
    data = np.random.random((10, 10))
    head = fits.Header()
    head["TEST"] = "foo"
    visp_science_task.intermediate_frame_helpers_write_arrays(
        arrays=data, headers=head, beam=1, map_scan=2, raster_step=3, task="BAR"
    )
    loaded_list = list(
        visp_science_task.read(
            tags=[
                VispTag.intermediate(),
                VispTag.frame(),
                VispTag.beam(1),
                VispTag.map_scan(2),
                VispTag.raster_step(3),
                VispTag.task("BAR"),
            ],
            decoder=fits_hdu_decoder,
        )
    )
    assert len(loaded_list) == 1
    hdu = loaded_list[0]
    np.testing.assert_equal(hdu.data, data)
    assert hdu.header["TEST"] == "foo"


def test_write_intermediate_arrays_none_header(visp_science_task):
    """
    Given: A VispTaskBase task
    When: Using the helper to write a single intermediate array with no header
    Then: The array is written and tagged correctly
    """
    data = np.random.random((10, 10))
    visp_science_task.intermediate_frame_helpers_write_arrays(
        arrays=data, headers=None, beam=1, map_scan=2, raster_step=3, task="BAR"
    )
    loaded_list = list(
        visp_science_task.read(
            tags=[
                VispTag.intermediate(),
                VispTag.frame(),
                VispTag.beam(1),
                VispTag.map_scan(2),
                VispTag.raster_step(3),
                VispTag.task("BAR"),
            ],
            decoder=fits_hdu_decoder,
        )
    )
    assert len(loaded_list) == 1
    hdu = loaded_list[0]
    np.testing.assert_equal(hdu.data, data)


def test_load_intermediate_arrays(visp_science_task):
    """
    Given: A Visp science task with intermediate frames
    When: Loading intermediate arrays
    Then: The correct arrays are returned
    """
    task = visp_science_task
    tag_fcns = [[VispTag.beam], [VispTag.readout_exp_time, VispTag.task], [VispTag.modstate]]
    tag_vals = [[1], [10.23, "dark"], [3]]
    tag_list = [[f(v) for f, v in zip(fl, vl)] for fl, vl in zip(tag_fcns, tag_vals)]

    for i, tags in enumerate(tag_list):
        data = np.ones((2, 2)) * i
        task.write(
            data=data,
            tags=tags + [VispTag.intermediate(), VispTag.frame()],
            encoder=fits_array_encoder,
        )

    for i, tags in enumerate(tag_list):
        arrays = list(task.intermediate_frame_helpers_load_intermediate_arrays(tags=tags))
        assert len(arrays) == 1
        np.testing.assert_equal(arrays[0], np.ones((2, 2)) * i)


def test_load_intermediate_dark_array():
    pass


def test_load_intermediate_lamp_gain_array():
    pass


def test_load_intermediate_solar_gain_array():
    pass


def test_load_intermediate_geometric_hdu_list():
    pass


def test_load_intermediate_demodulated_arrays():
    pass
