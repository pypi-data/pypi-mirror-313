"""Cases for testing ``test_find_entitlement_associations`` operation."""

import typing as t

import httpx
from connector.generated import (
    Error,
    ErrorCode,
    ErrorResponse,
    FindEntitlementAssociations,
    FindEntitlementAssociationsRequest,
    FindEntitlementAssociationsResponse,
)
from connector.utils.test import http_error_message
from {name}.integration import BASE_URL

from tests.common_mock_data import INVALID_AUTH, SETTINGS, VALID_AUTH
from connector.tests.type_definitions import MockedResponse, ResponseBodyMap

Case: t.TypeAlias = tuple[
    FindEntitlementAssociationsRequest,
    ResponseBodyMap,
    FindEntitlementAssociationsResponse | ErrorResponse,
]


def case_find_entitlement_associations_1_404() -> Case:
    """Authorized request for non-existing entitlement should fail."""
    args = FindEntitlementAssociationsRequest(
        request=FindEntitlementAssociations(),
        auth=VALID_AUTH,
        settings=SETTINGS,
    )
    response_body_map = {{
        "GET": {{
            "/": MockedResponse(
                status_code=httpx.codes.NOT_FOUND,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message=http_error_message(
                f"{{BASE_URL}}/",
                404,
            ),
            status_code=httpx.codes.NOT_FOUND,
            error_code=ErrorCode.NOT_FOUND,
            app_id="{name}",
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:find_entitlement_associations",
        ),
    )
    return args, response_body_map, expected_response


def case_find_entitlement_associations_1_200() -> Case:
    """Succeed with finding entitlement associations."""
    args = FindEntitlementAssociationsRequest(
        request=FindEntitlementAssociations(),
        auth=VALID_AUTH,
        settings=SETTINGS,
    )
    response_body_map = {{
        "GET": {{
            "/": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = FindEntitlementAssociationsResponse(
        response=[],
    )
    return args, response_body_map, expected_response


def case_find_entitlement_associations_1_empty_200() -> Case:
    """Succeed with getting empty entitlement associations."""
    args = FindEntitlementAssociationsRequest(
        request=FindEntitlementAssociations(),
        auth=VALID_AUTH,
        settings=SETTINGS,
    )
    response_body_map = {{
        "GET": {{
            "/": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = FindEntitlementAssociationsResponse(
        response=[],
    )
    return args, response_body_map, expected_response
