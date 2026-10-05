import pytest

from api_apiserver.auth import Auth
from api_apiserver.devices import DeviceApi


@pytest.fixture
def api():
    """Logged-in DeviceApi without a browser (API / DB tests).

    Append ids to `api.created_ids`; they are deleted after the test, pass or fail.
    """
    auth = Auth()
    device_api = DeviceApi(auth)
    yield device_api
    for device_id in device_api.created_ids:
        device_api.delete(
            device_id
        )  # 404 is fine: the test may have deleted it already
    auth.logout()
