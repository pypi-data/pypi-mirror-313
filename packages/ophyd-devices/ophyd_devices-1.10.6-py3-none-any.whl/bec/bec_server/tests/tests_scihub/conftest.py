import pytest
from py_scibec_openapi_client.models.beamline_with_relations import BeamlineWithRelations
from py_scibec_openapi_client.models.dataset_with_relations import DatasetWithRelations
from py_scibec_openapi_client.models.experiment_with_relations import ExperimentWithRelations
from py_scibec_openapi_client.models.scan_with_relations import ScanWithRelations

from bec_lib.logger import bec_logger

# overwrite threads_check fixture from bec_lib,
# to have it in autouse


@pytest.fixture(autouse=True)
def threads_check(threads_check):
    yield
    bec_logger.logger.remove()


@pytest.fixture()
def active_experiment():
    return ExperimentWithRelations(
        name="dummy_experiment",
        writeAccount="p12345",
        id="dummy_experiment_id",
        beamlineId="dummy_id",
    )


@pytest.fixture()
def beamline_document():
    return BeamlineWithRelations(
        name="dummy_bl", activeExperiment="dummy_experiment", id="dummy_id"
    )


@pytest.fixture()
def dataset_document():
    return DatasetWithRelations(name="dummy_dataset", id="dummy_id")


@pytest.fixture()
def scan_document():
    return ScanWithRelations(
        name="dummy_scan",
        id="dummy_id",
        readACL=["readACL"],
        writeACL=["writeACL"],
        owner=["owner"],
    )
