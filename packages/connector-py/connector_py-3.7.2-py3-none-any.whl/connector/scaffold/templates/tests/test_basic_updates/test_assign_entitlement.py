import json

import pytest
import pytest_cases
from connector.generated import (
    AssignEntitlementRequest,
    AssignEntitlementResponse,
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
        "tests.test_basic_updates.test_assign_entitlement_cases",
    ],
)
async def test_assign_entitlement(
    args: AssignEntitlementRequest,
    response_body_map: ResponseBodyMap,
    expected_response: AssignEntitlementResponse,
    httpx_mock: HTTPXMock,
) -> None:
    """Test ``assign-entitlement`` operation."""
    mock_requests(response_body_map, httpx_mock, host=BASE_URL)
    response = await integration.dispatch(CapabilityName.ASSIGN_ENTITLEMENT, args.model_dump_json())

    assert json.loads(response) == expected_response.model_dump()
