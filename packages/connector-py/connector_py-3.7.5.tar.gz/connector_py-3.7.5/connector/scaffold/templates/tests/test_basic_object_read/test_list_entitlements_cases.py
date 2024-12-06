"""Cases for testing ``list_entitlements`` operation."""

import typing as t

import httpx
from connector.generated import (
    Error,
    ErrorCode,
    ErrorResponse,
    ListEntitlements,
    ListEntitlementsRequest,
    ListEntitlementsResponse,
    Page,
)
from connector.utils.test import http_error_message

from tests.common_mock_data import INVALID_AUTH, SETTINGS, VALID_AUTH
from connector.tests.type_definitions import MockedResponse, ResponseBodyMap

Case: t.TypeAlias = tuple[
    ListEntitlementsRequest,
    ResponseBodyMap,
    ListEntitlementsResponse | ErrorResponse,
]


def case_list_entitlements_200() -> Case:
    """Successful request."""
    args = ListEntitlementsRequest(
        request=ListEntitlements(),
        auth=VALID_AUTH,
        settings=SETTINGS,
        page=Page(
            size=5,
        ),
    )
    response_body_map = {{
        "GET": {{
            "/example": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ListEntitlementsResponse(
        response=[],
    )
    return args, response_body_map, expected_response


INVALID_ARGS = ListEntitlementsRequest(
    request=ListEntitlements(),
    auth=INVALID_AUTH,
    settings=SETTINGS,
    page=Page(
        size=5,
    ),
)


def case_list_entitlements_400() -> Case:
    """Bad request should fail."""

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
            raised_in="{name}.integration:list_entitlements",
        ),
    )

    return INVALID_ARGS, response_body_map, expected_response
