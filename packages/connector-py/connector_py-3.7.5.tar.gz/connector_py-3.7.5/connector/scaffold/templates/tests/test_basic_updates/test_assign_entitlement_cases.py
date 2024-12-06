"""Cases for testing ``assign_entitlement`` operation."""

import typing as t

import httpx
from connector.generated import (
    AssignedEntitlement,
    AssignEntitlement,
    AssignEntitlementRequest,
    AssignEntitlementResponse,
    Error,
    ErrorCode,
    ErrorResponse,
)
from connector.utils.test import http_error_message

from tests.common_mock_data import INVALID_AUTH, SETTINGS, VALID_AUTH
from connector.tests.type_definitions import MockedResponse, ResponseBodyMap

Case: t.TypeAlias = tuple[
    AssignEntitlementRequest,
    ResponseBodyMap,
    AssignEntitlementResponse | ErrorResponse,
]

VALID_ASSIGN_REQUEST = AssignEntitlementRequest(
    request=AssignEntitlement(
        account_integration_specific_id="",
        resource_integration_specific_id="",
        resource_type="",
        entitlement_integration_specific_id="",
        entitlement_type="",
    ),
    auth=VALID_AUTH,
    settings=SETTINGS,
)
INVALID_ASSIGN_REQUEST = AssignEntitlementRequest(
    request=AssignEntitlement(
        account_integration_specific_id="",
        resource_integration_specific_id="",
        resource_type="",
        entitlement_integration_specific_id="",
        entitlement_type="",
    ),
    auth=INVALID_AUTH,
    settings=SETTINGS,
)


# repeat following cases for all entitlements

def case_assign_entitlement_1_404() -> Case:
    """Authorized request for non-existing entitlement should fail."""
    args = VALID_ASSIGN_REQUEST
    response_body_map = {{
        "GET": {{
            "/example": MockedResponse(
                status_code=httpx.codes.NOT_FOUND,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message=http_error_message(
                "",
                404,
            ),
            status_code=httpx.codes.NOT_FOUND,
            error_code=ErrorCode.NOT_FOUND,
            app_id="{name}",
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:unassign_entitlement",
        ),
    )
    return args, response_body_map, expected_response


def case_assign_entitlement_1_400() -> Case:
    """Authorized bad request should fail."""
    args = VALID_ASSIGN_REQUEST
    response_body_map = {{
        "GET": {{
            "/example": MockedResponse(
                status_code=httpx.codes.BAD_REQUEST,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message=http_error_message(
                "",
                400,
            ),
            status_code=httpx.codes.BAD_REQUEST,
            error_code=ErrorCode.BAD_REQUEST,
            app_id="{name}",
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:unassign_entitlement",
        ),
    )
    return args, response_body_map, expected_response


def case_assign_entitlement_1_200() -> Case:
    """Succeed with changing entitlement."""
    args = VALID_ASSIGN_REQUEST
    response_body_map = {{
        "GET": {{
            "/example": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = AssignEntitlementResponse(
        response=AssignedEntitlement(assigned=True),
    )
    return args, response_body_map, expected_response
