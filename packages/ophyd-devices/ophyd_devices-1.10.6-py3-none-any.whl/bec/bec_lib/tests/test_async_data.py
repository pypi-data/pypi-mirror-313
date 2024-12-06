from unittest import mock

import numpy as np
import pytest

from bec_lib import messages
from bec_lib.async_data import AsyncDataHandler
from bec_lib.endpoints import MessageEndpoints

# pylint: disable=protected-access
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name


@pytest.fixture
def async_data():
    producer = mock.MagicMock()
    yield AsyncDataHandler(producer)


def test_process_async_data_replace(async_data):
    data = [
        {
            "data": messages.DeviceMessage(
                signals={"data": {"value": np.zeros((10, 10))}},
                metadata={"async_update": "replace"},
            )
        }
        for ii in range(10)
    ]
    res = async_data.process_async_data(data)
    assert res["data"]["value"].shape == (10, 10)


def test_process_async_multiple_signals(async_data):
    data = [
        {
            "data": messages.DeviceMessage(
                signals={
                    "signal1": {"value": np.zeros((10, 10))},
                    "signal2": {"value": np.zeros((20, 20))},
                },
                metadata={"async_update": "replace"},
            )
        }
        for ii in range(10)
    ]
    res = async_data.process_async_data(data)
    assert res["signal1"]["value"].shape == (10, 10)
    assert res["signal2"]["value"].shape == (20, 20)


def test_process_async_data_extend(async_data):
    data = [
        {
            "data": messages.DeviceMessage(
                signals={"data": {"value": np.zeros((10, 10))}}, metadata={"async_update": "extend"}
            )
        }
        for ii in range(10)
    ]
    res = async_data.process_async_data(data)
    assert res["data"]["value"].shape == (100, 10)


def test_process_async_update_append(async_data):
    data = [
        {
            "data": messages.DeviceMessage(
                signals={"data": {"value": np.zeros((10, 10))}}, metadata={"async_update": "append"}
            )
        }
        for ii in range(10)
    ]
    res = async_data.process_async_data(data)
    assert res["data"]["value"][0].shape == (10, 10)
    assert len(res["data"]["value"]) == 10


def test_process_async_data_single(async_data):
    data = [
        {
            "data": messages.DeviceMessage(
                signals={"data": {"value": np.zeros((10, 10))}}, metadata={}
            )
        }
    ]
    res = async_data.process_async_data(data)
    assert res["data"]["value"].shape == (10, 10)


def test_get_async_data_for_scan():
    producer = mock.MagicMock()
    async_data = AsyncDataHandler(producer)
    producer.keys.return_value = [
        MessageEndpoints.device_async_readback("scan_id", "samx").endpoint.encode(),
        MessageEndpoints.device_async_readback("scan_id", "samy").endpoint.encode(),
    ]
    with mock.patch.object(async_data, "get_async_data_for_device") as mock_get:
        async_data.get_async_data_for_scan("scan_id")
        assert mock_get.call_count == 2


def test_get_async_data_for_device():
    producer = mock.MagicMock()
    async_data = AsyncDataHandler(producer)
    producer.xrange.return_value = [
        {
            "data": messages.DeviceMessage(
                signals={"data": {"value": np.zeros((10, 10))}}, metadata={}
            )
        }
    ]
    res = async_data.get_async_data_for_device("scan_id", "samx")
    assert res["data"]["value"].shape == (10, 10)
    assert len(res) == 1
    assert producer.xrange.call_count == 1
    producer.xrange.assert_called_with(
        MessageEndpoints.device_async_readback("scan_id", "samx"), min="-", max="+"
    )
