"""Cases for testing ``create_account`` operation."""

import typing as t

import httpx
from connector.generated import (
    AccountStatus,
    CreateAccount,
    CreateAccountEntitlement,
    CreateAccountRequest,
    CreateAccountResponse,
    CreatedAccount,
    Error,
    ErrorCode,
    ErrorResponse,
)
from connector.utils.test import http_error_message
from {name}.integration import BASE_URL

from tests.common_mock_data import INVALID_AUTH, SETTINGS, VALID_AUTH
from connector.tests.type_definitions import MockedResponse, ResponseBodyMap

Case: t.TypeAlias = tuple[
    CreateAccountRequest,
    ResponseBodyMap,
    CreateAccountResponse | ErrorResponse,
]


def case_create_account_201() -> Case:
    """Successful creation request."""
    args = CreateAccountRequest(
        request=CreateAccount(
            email="jw7rT@example.com",
            given_name="John",
            family_name="Doe",
            entitlements=[
                CreateAccountEntitlement(
                    integration_specific_id="read_only_user",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="role",
                ),
                CreateAccountEntitlement(
                    integration_specific_id="license-1",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="license",
                ),
            ],
        ),
        auth=VALID_AUTH,
        settings=SETTINGS,
    )
    user_id = "1"
    response_body = {{
        "user": {{
            "id": user_id,
            "email": args.request.email,
            "name": f"{{args.request.given_name}} {{args.request.family_name}}",
            "html_url": f"https://dev-lumos.{name}.com/users/{{user_id}}",
            "role": args.request.entitlements[0].integration_specific_id,
            "license": {{"id": args.request.entitlements[1].integration_specific_id}},
        }},
    }}
    response_body_map = {{
        "POST": {{
            "/users": MockedResponse(
                status_code=httpx.codes.CREATED,
                response_body=response_body,
            ),
        }},
    }}
    expected_response = CreateAccountResponse(
        response=CreatedAccount(created=True, status=AccountStatus.ACTIVE),
    )
    return args, response_body_map, expected_response


def case_create_account_400_missing_email() -> Case:
    """Invalid request when creating an account without user email."""
    args = CreateAccountRequest(
        request=CreateAccount(
            entitlements=[],
        ),
        auth=VALID_AUTH,
        settings=SETTINGS,
    )
    response_body_map = {{
        "POST": {{
            "/users": MockedResponse(
                status_code=httpx.codes.BAD_REQUEST,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="Email is required, provide 'email' in account data",
            error_code=ErrorCode.BAD_REQUEST,
            raised_by="ConnectorError",
            raised_in="{name}.integration:create_account",
            app_id="{name}",
        ),
    )
    return args, response_body_map, expected_response


def case_create_account_400_missing_name() -> Case:
    """Invalid request when creating an account without user given and family names."""
    args = CreateAccountRequest(
        request=CreateAccount(
            email="jw7rT@example.com",
            entitlements=[],
        ),
        auth=VALID_AUTH,
        settings=SETTINGS,
    )
    response_body_map = {{
        "POST": {{
            "/users": MockedResponse(
                status_code=httpx.codes.BAD_REQUEST,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="Name is required, provide both 'given_name' and 'family_name' in account data",
            error_code=ErrorCode.BAD_REQUEST,
            app_id="{name}",
            raised_by="ConnectorError",
            raised_in="{name}.integration:create_account",
        ),
    )
    return args, response_body_map, expected_response


def case_create_account_400_too_many_entitlements() -> Case:
    """Invalid request when creating an account with too many provided entitlements."""
    args = CreateAccountRequest(
        request=CreateAccount(
            email="jw7rT@example.com",
            given_name="John",
            family_name="Doe",
            entitlements=[
                CreateAccountEntitlement(
                    integration_specific_id="",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="",
                ),
                CreateAccountEntitlement(
                    integration_specific_id="",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="",
                ),
                CreateAccountEntitlement(
                    integration_specific_id="license-1",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="",
                ),
            ],
        ),
        auth=VALID_AUTH,
        settings=SETTINGS,
    )
    response_body_map = {{
        "POST": {{
            "/users": MockedResponse(
                status_code=httpx.codes.BAD_REQUEST,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="Too many entitlements provided",
            error_code=ErrorCode.BAD_REQUEST,
            app_id="{name}",
            raised_by="ConnectorError",
            raised_in="{name}.integration:create_account",
        ),
    )
    return args, response_body_map, expected_response


def case_create_account_400_invalid_entitlements() -> Case:
    """Invalid request when creating an account with too many provided entitlements."""
    args = CreateAccountRequest(
        request=CreateAccount(
            email="jw7rT@example.com",
            given_name="John",
            family_name="Doe",
            entitlements=[
                CreateAccountEntitlement(
                    integration_specific_id="",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="",
                ),
                CreateAccountEntitlement(
                    integration_specific_id="",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="",
                ),
            ],
        ),
        auth=VALID_AUTH,
        settings=SETTINGS,
    )
    response_body_map = {{
        "POST": {{
            "/users": MockedResponse(
                status_code=httpx.codes.BAD_REQUEST,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="The same entitlement type provided",
            error_code=ErrorCode.BAD_REQUEST,
            app_id="{name}",
            raised_by="ConnectorError",
            raised_in="{name}.integration:create_account",
        ),
    )
    return args, response_body_map, expected_response
