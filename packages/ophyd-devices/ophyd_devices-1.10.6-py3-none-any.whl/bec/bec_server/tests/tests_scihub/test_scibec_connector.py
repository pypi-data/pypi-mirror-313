from unittest import mock

import pytest

from bec_lib import messages
from bec_lib.endpoints import MessageEndpoints
from bec_lib.messages import BECStatus
from bec_lib.service_config import ServiceConfig
from bec_lib.tests.utils import ConnectorMock
from bec_server.scihub import SciHub
from bec_server.scihub.scibec import SciBecConnector


class SciHubMocked(SciHub):
    def _start_metrics_emitter(self):
        pass

    def wait_for_service(self, name, status=BECStatus.RUNNING):
        pass

    def _start_scibec_connector(self):
        pass

    def _start_scilog_connector(self):
        pass


@pytest.fixture()
def SciHubMock():
    config = ServiceConfig(
        redis={"host": "dummy", "port": 6379},
        service_config={
            "file_writer": {"plugin": "default_NeXus_format", "base_path": "./"},
            "log_writer": {"base_path": "./"},
        },
    )
    scihub_mocked = SciHubMocked(config, ConnectorMock)
    yield scihub_mocked
    scihub_mocked.shutdown()


@pytest.fixture()
def SciBecMock(SciHubMock):
    with mock.patch.object(SciBecConnector, "_start"):
        scibec_mock = SciBecConnector(SciHubMock, SciHubMock.connector)
        yield scibec_mock
        scibec_mock.shutdown()


def test_scibec_connector(SciHubMock):
    with mock.patch.object(SciBecConnector, "connect_to_scibec") as mock_connect_to_scibec:
        scibec_connector = SciBecConnector(SciHubMock, SciHubMock.connector)
        mock_connect_to_scibec.assert_called_once()


def test_scibec_load_environment(SciBecMock):
    with mock.patch("os.path.exists", side_effect=[False, True]):
        with mock.patch(
            "bec_server.scihub.scibec.scibec_connector.dotenv_values"
        ) as mock_dotenv_values:
            with mock.patch.object(SciBecMock, "_update_config") as mock_update_config:
                mock_dotenv_values.return_value = {
                    "SCIBEC_HOST": "dummy_host",
                    "SCIBEC_TARGET": "dummy_bl",
                    "SCIBEC_INGESTOR": "dummy_ingestor",
                    "SCIBEC_INGESTOR_SECRET": "dummy_ingestor_secret",
                    "SCIBEC_RO_USER": "dummy_ro_user",
                    "SCIBEC_RO_USER_SECRET": "dummy_ro_user_secret",
                }
                SciBecMock._load_environment()
                mock_dotenv_values.assert_called_once()
                mock_update_config.assert_called_once_with(
                    SCIBEC_HOST="dummy_host",
                    SCIBEC_TARGET="dummy_bl",
                    SCIBEC_INGESTOR="dummy_ingestor",
                    SCIBEC_INGESTOR_SECRET="dummy_ingestor_secret",
                    SCIBEC_RO_USER="dummy_ro_user",
                    SCIBEC_RO_USER_SECRET="dummy_ro_user_secret",
                )


def test_scibec_update_config(SciBecMock):
    SciBecMock._update_config(
        SCIBEC_HOST="dummy_host",
        SCIBEC_TARGET="dummy_bl",
        SCIBEC_INGESTOR="dummy_ingestor",
        SCIBEC_INGESTOR_SECRET="dummy_ingestor_secret",
        SCIBEC_RO_USER="dummy_ro_user",
        SCIBEC_RO_USER_SECRET="dummy_ro_user_secret",
    )
    assert SciBecMock.host == "dummy_host"
    assert SciBecMock.target_bl == "dummy_bl"
    assert SciBecMock.ingestor == "dummy_ingestor"
    assert SciBecMock.ingestor_secret == "dummy_ingestor_secret"
    assert SciBecMock.ro_user == "dummy_ro_user"
    assert SciBecMock.ro_user_secret == "dummy_ro_user_secret"
    assert SciBecMock._env_configured == True


def test_scibec_connect_to_scibec(SciBecMock):
    with mock.patch.object(SciBecMock, "_load_environment"):
        SciBecMock._env_configured = True
        with mock.patch.object(
            SciBecMock, "_update_scibec_instance"
        ) as mock_update_scibec_instance:
            with mock.patch.object(
                SciBecMock, "_update_experiment_info"
            ) as mock_update_experiment_info:
                with mock.patch.object(
                    SciBecMock, "_update_eaccount_in_redis"
                ) as mock_update_eaccount_in_redis:
                    SciBecMock.connect_to_scibec()
                    mock_update_scibec_instance.assert_called_once()
                    mock_update_experiment_info.assert_called_once()
                    mock_update_eaccount_in_redis.assert_called_once()


def test_scibec_update_experiment_info(SciBecMock, active_experiment, beamline_document):
    with mock.patch.object(SciBecMock, "scibec") as mock_scibec:
        mock_scibec.beamline.beamline_controller_find.return_value = (beamline_document,)
        experiment_document = active_experiment
        mock_scibec.experiment.experiment_controller_find_by_id.return_value = experiment_document
        SciBecMock._update_experiment_info()
        assert SciBecMock.scibec_info["activeExperiment"] == experiment_document
        assert SciBecMock.scibec_info["beamline"] == beamline_document


def test_update_eaccount_in_redis(SciBecMock, active_experiment):
    SciBecMock.scibec_info = {"activeExperiment": active_experiment}
    with mock.patch.object(SciBecMock, "connector") as mock_connector:
        SciBecMock._update_eaccount_in_redis()
        mock_connector.set.assert_called_once_with(
            MessageEndpoints.account(), messages.VariableMessage(value="e12345")
        )
