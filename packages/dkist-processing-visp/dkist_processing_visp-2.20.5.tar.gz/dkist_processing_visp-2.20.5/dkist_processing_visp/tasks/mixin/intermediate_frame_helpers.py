"""Helper to manage intermediate data."""
import itertools
from typing import Generator
from typing import Iterable
from typing import TypeVar

import numpy as np
from astropy.io import fits
from dkist_processing_common.codecs.fits import fits_array_decoder
from dkist_processing_common.codecs.fits import fits_array_encoder
from dkist_processing_common.models.fits_access import FitsAccessBase
from dkist_service_configuration.logging import logger

from dkist_processing_visp.models.tags import VispTag


class IntermediateFrameHelpersMixin:
    """Mixin for methods that support easy loading and writing of intermediate frames."""

    F = TypeVar("F", bound=FitsAccessBase)

    def intermediate_frame_helpers_write_arrays(
        self,
        arrays: Iterable[np.ndarray] | np.ndarray,
        headers: Iterable[fits.Header] | fits.Header | None = None,
        beam: int | None = None,
        modstate: int | None = None,
        map_scan: int | None = None,
        raster_step: int | None = None,
        exposure_time: float | None = None,
        readout_exp_time: float | None = None,
        task: str | None = None,
        task_tag: str | None = None,
    ) -> None:
        """
        Write out intermediate files with requested tags.

        Parameters
        ----------
        arrays
            pass

        headers
            pass

        beam : int
            The current beam being processed

        modstate : int
            The current modulator state

        map_scan : int
             The current map scan

        raster_step : int
            The slit step for this step

        task : str
            The task type of the data currently being processed

        exposure_time : float
            The FPA exposure time

        readout_exp_time
            Exposure time of a single readout

        file_id:
            The unique file_id

        Returns
        -------
        None
        """
        if task_tag is not None and task is not None:
            raise ValueError("Cannot specify both the raw 'task' and a formatted 'task_tag'.")
        if task_tag is None and task is None:
            raise ValueError("Must specify exactly one of raw 'task' or formatted 'task_tag'.")

        if task is not None:
            task_tag = VispTag.task(task)
        tags = [VispTag.intermediate(), VispTag.frame(), task_tag]

        for arg, tag_func in zip(
            [beam, modstate, map_scan, raster_step, exposure_time, readout_exp_time],
            [
                VispTag.beam,
                VispTag.modstate,
                VispTag.map_scan,
                VispTag.raster_step,
                VispTag.exposure_time,
                VispTag.readout_exp_time,
            ],
        ):
            if arg is not None:
                tags.append(tag_func(arg))

        arrays = [arrays] if isinstance(arrays, np.ndarray) else arrays
        if headers is not None:
            headers = [headers] if isinstance(headers, fits.Header) else headers
        else:
            headers = itertools.repeat(None)

        filenames = []
        for array, header in zip(arrays, headers):
            written_path = self.write(
                data=array, header=header, encoder=fits_array_encoder, tags=tags
            )
            filenames.append(str(written_path))

        logger.info(f"Wrote intermediate file(s) for {tags = } to {filenames}")

    def intermediate_frame_helpers_load_intermediate_arrays(
        self, tags: [str]
    ) -> Generator[np.ndarray, None, None]:
        """Yield a generator that produces ndarrays for the requested tags."""
        tags = list(set([VispTag.intermediate(), VispTag.frame()] + tags))

        if self.scratch.count_all(tags=tags) == 0:
            raise FileNotFoundError(f"No files found matching {tags =}")

        yield from self.read(decoder=fits_array_decoder, tags=tags)

    def intermediate_frame_helpers_load_dark_array(
        self,
        *,
        beam: int,
        exposure_time: float | None = None,
        readout_exp_time: float | None = None,
    ) -> np.ndarray:
        """
        Produce dark ndarrays for the requested tags.

        Parameters
        ----------
        beam : int
            The current beam being processed

        exposure_time : float
            The FPA exposure time

        readout_exp_time
            Exposure time of a single readout

        Returns
        -------
        ndarray
            Array of loaded intermediate dark data with requested tags
        """
        tags = [VispTag.task_dark(), VispTag.beam(beam)]

        if exposure_time is not None:
            tags.append(VispTag.exposure_time(exposure_time))

        if readout_exp_time is not None:
            tags.append(VispTag.readout_exp_time(readout_exp_time))

        return next(self.intermediate_frame_helpers_load_intermediate_arrays(tags=tags))

    def intermediate_frame_helpers_load_background_array(self, *, beam: int) -> np.ndarray:
        """
        Produce background light ndarrays for the requested tags.

        Parameters
        ----------
        beam : int
            The current beam being processed

        Returns
        -------
        ndarray
            Array of loaded intermediate background light data with requested tags
        """
        tags = [VispTag.task_background(), VispTag.beam(beam)]

        return next(self.intermediate_frame_helpers_load_intermediate_arrays(tags=tags))

    def intermediate_frame_helpers_load_lamp_gain_array(
        self, *, beam: int, modstate: int
    ) -> np.ndarray:
        """
        Produce lamp gain ndarrays for the requested tags.

        Parameters
        ----------
        beam : int
            The current beam being processed
        modstate : int
            The current modulator state


        Returns
        -------
        ndarray
            Array of loaded intermediate lamp gain data with requested tags
        """
        tags = [VispTag.task_lamp_gain(), VispTag.beam(beam), VispTag.modstate(modstate)]

        return next(self.intermediate_frame_helpers_load_intermediate_arrays(tags=tags))

    def intermediate_frame_helpers_load_solar_gain_array(
        self, *, beam: int, modstate: int
    ) -> np.ndarray:
        """
        Produce solar gain ndarrays for the requested tags.

        Parameters
        ----------
        beam : int
            The current beam being processed
        modstate : int
            The current modulator state


        Returns
        -------
        ndarray
            Array of loaded intermediate solar gain data with requested tags
        """
        tags = [VispTag.task_solar_gain(), VispTag.beam(beam), VispTag.modstate(modstate)]

        return next(self.intermediate_frame_helpers_load_intermediate_arrays(tags=tags))

    def intermediate_frame_helpers_load_demod_matrices(self, *, beam_num: int) -> np.ndarray:
        """
        Load demodulated matrices.

        Parameters
        ----------
        beam_num : int
            The current beam being processed


        Returns
        -------
        ndarray
            Demodulated matrix data
        """
        tags = [
            VispTag.task_demodulation_matrices(),
            VispTag.beam(beam_num),
        ]
        array = next(self.intermediate_frame_helpers_load_intermediate_arrays(tags=tags))
        return array

    def intermediate_frame_helpers_load_angle(self, *, beam: int) -> float:
        """
        Load geometric angle for a given frame (beam).

        Parameters
        ----------
        beam : int
            The current beam being processed

        Returns
        -------
        float
            angle
        """
        tags = [VispTag.task_geometric_angle(), VispTag.beam(beam)]
        angle_array = next(self.intermediate_frame_helpers_load_intermediate_arrays(tags=tags))
        return angle_array[0]

    def intermediate_frame_helpers_load_state_offset(
        self, *, beam: int, modstate: int
    ) -> np.ndarray:
        """
        Load state offset for a given beam and modstate.

        Parameters
        ----------
        beam : int
            The current beam being processed
        modstate : int
            The current modulator state


        Returns
        -------
        ndarray
            state offset array
        """
        tags = [VispTag.task_geometric_offset(), VispTag.beam(beam), VispTag.modstate(modstate)]
        offset = next(self.intermediate_frame_helpers_load_intermediate_arrays(tags=tags))
        return offset

    def intermediate_frame_helpers_load_spec_shift(self, *, beam: int) -> np.ndarray:
        """
        Load spectral shift for a given beam.

        Parameters
        ----------
        beam : int
            The current beam being processed


        Returns
        -------
        ndarray
            spectral shift array
        """
        tags = [VispTag.task_geometric_sepectral_shifts(), VispTag.beam(beam)]
        shifts = next(self.intermediate_frame_helpers_load_intermediate_arrays(tags=tags))
        return shifts
