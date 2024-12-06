import pytest
import pytest_cases
from connector.generated import (
    GetLastActivityRequest,
    GetLastActivityResponse,
)
from connector.tests.mock_httpx import mock_requests
from connector.oai.capability import CapabilityName
from {name}.integration import integration, BASE_URL

from connector.tests.type_definitions import ResponseBodyMap
from pytest_httpx import HTTPXMock

@pytest.mark.skip(
    reason="Function not implemented yet, remove after implementation of tested function."
)
@pytest_cases.parametrize_with_cases(
    ["args", "response_body_map", "expected_response"],
    cases=[
        "tests.test_get_last_activity.test_get_last_activity_cases",
    ],
)
async def test_get_last_activity(
    args: GetLastActivityRequest,
    response_body_map: ResponseBodyMap,
    expected_response: GetLastActivityResponse,
    httpx_mock: HTTPXMock,
) -> None:
    mock_requests(response_body_map, httpx_mock, host=BASE_URL)
    response = await integration.dispatch(CapabilityName.GET_LAST_ACTIVITY, args.model_dump_json())

    assert response == expected_response.model_dump_json()
