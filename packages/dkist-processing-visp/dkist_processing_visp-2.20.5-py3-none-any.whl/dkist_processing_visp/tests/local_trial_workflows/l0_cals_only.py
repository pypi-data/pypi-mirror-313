import argparse
import json
import os
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from random import randint

from astropy.io import fits
from dkist_header_validator import spec122_validator
from dkist_processing_common.manual import ManualProcessing
from dkist_processing_common.tasks import WorkflowTaskBase
from dkist_service_configuration.logging import logger

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.tasks.background_light import BackgroundLightCalibration
from dkist_processing_visp.tasks.dark import DarkCalibration
from dkist_processing_visp.tasks.geometric import GeometricCalibration
from dkist_processing_visp.tasks.instrument_polarization import InstrumentPolarizationCalibration
from dkist_processing_visp.tasks.lamp import LampCalibration
from dkist_processing_visp.tasks.solar import SolarCalibration
from dkist_processing_visp.tests.conftest import VispInputDatasetParameterValues
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import LoadBackgroundCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import LoadDarkCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import LoadGeometricCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import LoadInputParsing
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import LoadInstPolCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import LoadLampCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import LoadSolarCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import (
    ParseCalOnlyL0InputData,
)
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import SaveBackgroundCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import SaveDarkCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import SaveGeometricCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import SaveInputParsing
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import SaveInstPolCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import SaveLampCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import SaveSolarCal
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import (
    set_observe_wavelength_task,
)
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import SetNumModstates
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import SetObserveExpTime
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import (
    SetObserveIpStartTime,
)
from dkist_processing_visp.tests.local_trial_workflows.local_trial_helpers import SetPolarimeterMode


class DatetimeEncoder(json.JSONEncoder):
    # Copied from quality_report_maker
    """
    A JSON encoder which encodes datetime(s) as iso formatted strings.
    """

    def default(self, obj):
        if isinstance(obj, datetime):
            return {"iso_date": obj.isoformat("T")}
        return super().default(obj)


class Translate122To214L0(WorkflowTaskBase):
    def run(self) -> None:
        raw_dir = Path(self.scratch.scratch_base_path) / f"VISP{self.recipe_run_id:03n}"
        if not os.path.exists(self.scratch.workflow_base_path):
            os.makedirs(self.scratch.workflow_base_path)

        if not raw_dir.exists():
            raise FileNotFoundError(
                f"Expected to find a raw VISP{{run_id:03n}} folder in {self.scratch.scratch_base_path}"
            )

        for file in raw_dir.glob("*.FITS"):
            translated_file_name = Path(self.scratch.workflow_base_path) / os.path.basename(file)
            logger.info(f"Translating {file} -> {translated_file_name}")
            hdl = fits.open(file)

            header = spec122_validator.validate_and_translate_to_214_l0(
                hdl[0].header, return_type=fits.HDUList
            )[0].header

            comp_hdu = fits.CompImageHDU(header=header, data=hdl[0].data)
            comp_hdl = fits.HDUList([fits.PrimaryHDU(), comp_hdu])
            comp_hdl.writeto(translated_file_name, overwrite=True)

            hdl.close()
            del hdl
            comp_hdl.close()
            del comp_hdl


class CreateInputDatasetParameterDocument(WorkflowTaskBase):
    def run(self) -> None:
        doc_path = self.scratch.workflow_base_path / "input_dataset_parameters.json"
        with open(doc_path, "w") as f:
            f.write(json.dumps(self.input_dataset_document_simple_parameters_part))
        self.tag(doc_path, VispTag.input_dataset_parameters())
        logger.info(f"Wrote input dataset doc to {doc_path}")

    @property
    def input_dataset_document_simple_parameters_part(self):
        parameters_list = []
        value_id = randint(1000, 2000)
        for pn, pv in asdict(
            VispInputDatasetParameterValues(
                visp_background_on=False, visp_geo_upsample_factor=10000
            )
        ).items():
            values = [
                {
                    "parameterValueId": value_id,
                    "parameterValue": json.dumps(pv),
                    "parameterValueStartDate": "1946-11-20",
                }
            ]
            parameter = {"parameterName": pn, "parameterValues": values}
            parameters_list.append(parameter)

        return parameters_list


def tag_inputs_task(suffix: str):
    class TagInputs(WorkflowTaskBase):
        def run(self) -> None:
            logger.info(f"Looking in {os.path.abspath(self.scratch.workflow_base_path)}")
            input_file_list = list(self.scratch.workflow_base_path.glob(f"*.{suffix}"))
            if len(input_file_list) == 0:
                raise FileNotFoundError(
                    f"Did not find any files matching '*.{suffix}' in {self.scratch.workflow_base_path}"
                )
            for file in input_file_list:
                logger.info(f"Found {file}")
                self.tag(path=file, tags=[VispTag.input(), VispTag.frame()])

    return TagInputs


def setup_APM_config() -> None:
    mesh_config = {
        "system-monitoring-log-apm": {
            "mesh_address": "system-monitoring-log-apm.service.sim.consul",
            "mesh_port": 8200,
        },
        "automated-processing-scratch-inventory": {"mesh_address": "localhost", "mesh_port": 6379},
        "internal-api-gateway": {"mesh_address": "localhost", "mesh_port": 80},
    }
    apm_options = {"TRANSACTION_MAX_SPANS": 10000}
    os.environ["MESH_CONFIG"] = json.dumps(mesh_config)
    os.environ["ELASTIC_APM_ENABLED"] = "true"
    os.environ["ELASTIC_APM_OTHER_OPTIONS"] = json.dumps(apm_options)


def main(
    scratch_path: str,
    suffix: str = "FITS",
    recipe_run_id: int = 2,
    skip_translation: bool = False,
    only_translate: bool = False,
    load_input_parsing: bool = False,
    load_dark: bool = False,
    load_background: bool = False,
    load_lamp: bool = False,
    load_geometric: bool = False,
    load_solar: bool = False,
    load_inst_pol: bool = False,
    use_apm: bool = False,
    dummy_wavelength: float = 630.0,
):
    if use_apm:
        setup_APM_config()
    with ManualProcessing(
        workflow_path=scratch_path,
        recipe_run_id=recipe_run_id,
        testing=True,
        workflow_name="visp-l0-pipeline",
        workflow_version="GROGU",
    ) as manual_processing_run:
        if not skip_translation:
            manual_processing_run.run_task(task=Translate122To214L0)
        if only_translate:
            return
        manual_processing_run.run_task(task=CreateInputDatasetParameterDocument)

        if load_input_parsing:
            manual_processing_run.run_task(task=LoadInputParsing)
        else:
            manual_processing_run.run_task(task=tag_inputs_task(suffix))
            manual_processing_run.run_task(task=ParseCalOnlyL0InputData)
            manual_processing_run.run_task(
                task=set_observe_wavelength_task(wavelength=dummy_wavelength)
            )
            manual_processing_run.run_task(task=SetObserveIpStartTime)
            manual_processing_run.run_task(task=SetObserveExpTime)
            manual_processing_run.run_task(task=SetPolarimeterMode)
            manual_processing_run.run_task(task=SetNumModstates)
            manual_processing_run.run_task(task=SaveInputParsing)

        if load_dark:
            manual_processing_run.run_task(task=LoadDarkCal)
        else:
            manual_processing_run.run_task(task=DarkCalibration)
            manual_processing_run.run_task(task=SaveDarkCal)

        if load_background:
            manual_processing_run.run_task(task=LoadBackgroundCal)
        else:
            manual_processing_run.run_task(task=BackgroundLightCalibration)
            manual_processing_run.run_task(task=SaveBackgroundCal)

        if load_lamp:
            manual_processing_run.run_task(task=LoadLampCal)
        else:
            manual_processing_run.run_task(task=LampCalibration)
            manual_processing_run.run_task(task=SaveLampCal)

        if load_geometric:
            manual_processing_run.run_task(task=LoadGeometricCal)
        else:
            manual_processing_run.run_task(task=GeometricCalibration)
            manual_processing_run.run_task(task=SaveGeometricCal)

        if load_solar:
            manual_processing_run.run_task(task=LoadSolarCal)
        else:
            manual_processing_run.run_task(task=SolarCalibration)
            manual_processing_run.run_task(task=SaveSolarCal)

        if load_inst_pol:
            manual_processing_run.run_task(task=LoadInstPolCal)
        else:
            manual_processing_run.run_task(task=InstrumentPolarizationCalibration)
            manual_processing_run.run_task(task=SaveInstPolCal)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run an end-to-end test of the ViSP DC Science pipeline"
    )
    parser.add_argument("scratch_path", help="Location to use as the DC 'scratch' disk")
    parser.add_argument(
        "-i",
        "--run-id",
        help="Which subdir to use. This will become the recipe run id",
        type=int,
        default=4,
    )
    parser.add_argument("--suffix", help="File suffix to treat as INPUT frames", default="FITS")
    parser.add_argument(
        "-w",
        "--wavelength",
        help="Dummy wavelength to use for loading parameters, etc.",
        type=float,
        default=630.0,
    )
    parser.add_argument(
        "-T",
        "--skip-translation",
        help="Skip the translation of raw 122 l0 frames to 214 l0",
        action="store_true",
    )
    parser.add_argument(
        "-t", "--only-translate", help="Do ONLY the translation step", action="store_true"
    )
    parser.add_argument(
        "-I", "--load-input-parsing", help="Load tags on input files", action="store_true"
    )
    parser.add_argument(
        "-D",
        "--load-dark",
        help="Load dark calibration from previously saved run",
        action="store_true",
    )
    parser.add_argument(
        "-B",
        "--load-background",
        help="Load background light calibration from previously saved run",
        action="store_true",
    )
    parser.add_argument(
        "-L",
        "--load-lamp",
        help="Load lamp calibration from previously saved run",
        action="store_true",
    )
    parser.add_argument(
        "-G",
        "--load-geometric",
        help="Load geometric calibration from previously saved run",
        action="store_true",
    )
    parser.add_argument(
        "-S",
        "--load-solar",
        help="Load solar calibration from previously saved run",
        action="store_true",
    )
    parser.add_argument(
        "-P",
        "--load-inst-pol",
        help="Load instrument polarization calibration from previously saved run",
        action="store_true",
    )
    parser.add_argument("-A", "--use-apm", help="Send APM spans to SIM", action="store_true")
    args = parser.parse_args()
    sys.exit(
        main(
            scratch_path=args.scratch_path,
            suffix=args.suffix,
            recipe_run_id=args.run_id,
            skip_translation=args.skip_translation,
            only_translate=args.only_translate,
            load_input_parsing=args.load_input_parsing,
            load_dark=args.load_dark,
            load_background=args.load_background,
            load_lamp=args.load_lamp,
            load_geometric=args.load_geometric,
            load_solar=args.load_solar,
            load_inst_pol=args.load_inst_pol,
            use_apm=args.use_apm,
        )
    )
