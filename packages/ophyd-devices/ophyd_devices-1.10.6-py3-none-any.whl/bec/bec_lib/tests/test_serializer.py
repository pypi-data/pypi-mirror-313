import numpy as np
import pytest

from bec_lib.endpoints import MessageEndpoints
from bec_lib.messages import DeviceMessage
from bec_lib.serialization import json_ext, msgpack


@pytest.fixture(params=[json_ext, msgpack])
def serializer(request):
    yield request.param


@pytest.mark.parametrize(
    "data",
    [
        {"a": 1, "b": 2},
        "hello",
        1,
        1.0,
        [1, 2, 3],
        np.array([1, 2, 3]),
        {1, 2, 3},
        {
            "hroz": {
                "hroz": {"value": 0, "timestamp": 1708336264.5731058},
                "hroz_setpoint": {"value": 0, "timestamp": 1708336264.573121},
            }
        },
        MessageEndpoints.progress("test"),
        DeviceMessage,
        float,
    ],
)
def test_serialize(serializer, data):
    res = serializer.loads(serializer.dumps(data)) == data
    assert all(res) if isinstance(data, np.ndarray) else res
