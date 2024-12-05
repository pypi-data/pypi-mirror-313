"""Utilities for describing capabilities.

Each known capability is assigned a base class for request and response.
The actual request and response types in a integration implementation
can either use the base classes directly or create subclasses, however,
those bases are enforced to be used.
"""

import inspect
import typing as t

from pydantic import BaseModel, ValidationError

from connector.generated import (
    ActivateAccountRequest,
    ActivateAccountResponse,
    AssignEntitlementRequest,
    AssignEntitlementResponse,
    BasicCredential,
    CapabilityName,
    CapabilitySchema,
    CreateAccountRequest,
    CreateAccountResponse,
    DeactivateAccountRequest,
    DeactivateAccountResponse,
    DeleteAccountRequest,
    DeleteAccountResponse,
    ErrorCode,
    FindEntitlementAssociationsRequest,
    FindEntitlementAssociationsResponse,
    GetAuthorizationUrlRequest,
    GetAuthorizationUrlResponse,
    GetLastActivityRequest,
    GetLastActivityResponse,
    HandleAuthorizationCallbackRequest,
    HandleAuthorizationCallbackResponse,
    HandleClientCredentialsRequest,
    HandleClientCredentialsResponse,
    ListAccountsRequest,
    ListAccountsResponse,
    ListCustomAttributesSchemaRequest,
    ListCustomAttributesSchemaResponse,
    ListEntitlementsRequest,
    ListEntitlementsResponse,
    ListResourcesRequest,
    ListResourcesResponse,
    OAuthCredential,
    Page,
    RefreshAccessTokenRequest,
    RefreshAccessTokenResponse,
    TokenCredential,
    UnassignEntitlementRequest,
    UnassignEntitlementResponse,
    ValidateCredentialsRequest,
    ValidateCredentialsResponse,
)
from connector.oai.errors import ConnectorError


class Request(t.Protocol):
    auth: t.Any
    request: t.Any
    page: t.Any
    include_raw_data: t.Optional[bool] = None
    settings: t.Any


class AuthRequest(t.Protocol):
    request: t.Any
    page: t.Any
    include_raw_data: t.Optional[bool] = None
    settings: t.Any


def get_oauth(request: Request) -> OAuthCredential:
    if request.auth and request.auth.oauth and isinstance(request.auth.oauth, OAuthCredential):
        return request.auth.oauth
    raise ConnectorError(message="Wrong auth", error_code=ErrorCode.BAD_REQUEST)


def get_basic_auth(request: Request) -> BasicCredential:
    if request.auth and request.auth.basic and isinstance(request.auth.basic, BasicCredential):
        return request.auth.basic
    raise ConnectorError(message="Wrong auth", error_code=ErrorCode.BAD_REQUEST)


def get_token_auth(request: Request) -> TokenCredential:
    if request.auth and request.auth.token and isinstance(request.auth.token, TokenCredential):
        return request.auth.token
    raise ConnectorError(message="Wrong auth", error_code=ErrorCode.BAD_REQUEST)


def get_page(request: Request) -> Page:
    if request.page:
        return request.page
    return Page()


SettingsType = t.TypeVar("SettingsType", bound=BaseModel)


def get_settings(request: Request | AuthRequest, model: t.Type[SettingsType]) -> SettingsType:
    try:
        return model.model_validate(request.settings or {})
    except ValidationError as err:
        raise ConnectorError(
            message="Invalid request settings", error_code=ErrorCode.BAD_REQUEST
        ) from err


def extra_data(extra: dict[str, t.Any]) -> dict[str, str]:
    ret: dict[str, str] = {}
    for key, value in extra.items():
        if value:
            ret[key] = str(value)
    return ret


T = t.TypeVar("T")


class Response(t.Protocol):
    response: t.Any
    raw_data: t.Optional[t.Any]


_Request = t.TypeVar("_Request", bound=Request, contravariant=True)


class CapabilityCallableProto(t.Protocol, t.Generic[_Request]):
    def __call__(self, args: _Request) -> Response | t.Awaitable[Response]:
        ...

    __name__: str


class Empty(BaseModel):
    pass


def generate_capability_schema(
    capability_name: CapabilityName,
    impl: (CapabilityCallableProto[t.Any]),
) -> CapabilitySchema:
    request_annotation, response_annotation = get_capability_annotations(impl)
    request_type = _request_payload_type(request_annotation)
    response_type = _response_payload_type(response_annotation)
    if type(request_type) == type(t.Dict[str, t.Any]):  # noqa: E721
        request_type = Empty
    if type(response_type) == type(t.Dict[str, t.Any]):  # noqa: E721
        response_type = Empty
    return CapabilitySchema(
        argument=request_type.model_json_schema(),
        output=response_type.model_json_schema(),
    )


def get_capability_annotations(
    impl: CapabilityCallableProto[t.Any],
) -> t.Tuple[t.Any, t.Any]:
    """Extract argument and return type annotations."""
    annotations = inspect.get_annotations(impl)
    try:
        response_annotation = annotations["return"]
        request_annotation_name = (set(annotations.keys()) - {"return"}).pop()
    except KeyError:
        raise TypeError(
            f"The capability function {impl.__name__} must have both request and return annotations."
        ) from None

    request_annotation = annotations[request_annotation_name]

    return request_annotation, response_annotation


def _request_payload_type(model: t.Any) -> t.Any:
    if not hasattr(model, "model_fields"):
        raise TypeError(f"Not a pydantic model: {model}")
    return model.model_fields["request"].annotation


def _response_payload_type(model: t.Any) -> t.Any:
    if not hasattr(model, "model_fields"):
        raise TypeError(f"Not a pydantic model: {model}")
    return model.model_fields["response"].annotation


def _pluck_generic_parameter(type_annotation: t.Any) -> t.Any:
    if type(type_annotation) in (type(t.List[t.Any]), type(t.Dict[t.Any, t.Any])):
        value_type = type_annotation.__args__[-1]
        return value_type
    return type_annotation


def validate_capability(
    capability_name: CapabilityName,
    impl: (CapabilityCallableProto[t.Any]),
) -> None:
    """Make sure copability implementation is valid.

    Capability is marked as valid when:
        * is fully annotated, i.e., both argument and return value are
        type-hinted
        * type of accepted argument matches the expected one, i.e., is
        exactly the same class or a subclass
        * type of returned value matches the expected one, same
        mechanism as for argument
    """
    actual_request, actual_response = get_capability_annotations(impl)
    expected_request, expected_response = CAPABILITY_PAYLOADS[capability_name]
    if actual_response != expected_response:
        raise TypeError(
            f"The function {impl.__name__} for capability {capability_name} must return {expected_response.__name__}. "
            f"Actual response model: {actual_response.__name__}"
        ) from None

    actual_request_model = _pluck_generic_parameter(_request_payload_type(actual_request))
    expected_request_model = _pluck_generic_parameter(_request_payload_type(expected_request))

    if not issubclass(actual_request_model, expected_request_model):
        raise TypeError(
            f"The function {impl.__name__} for capability {capability_name} must accept {expected_request_model.__name__} "
            f"or its subclass. Actual request model: {actual_request_model.__name__}"
        ) from None


def capability_requires_auth(capability_name: str | CapabilityName) -> bool:
    capability_name = (
        capability_name
        if isinstance(capability_name, CapabilityName)
        else CapabilityName[capability_name]
    )
    expected_request, _ = CAPABILITY_PAYLOADS[capability_name]
    return (
        "auth" in expected_request.model_fields
        and expected_request.model_fields["auth"].is_required
    )


CAPABILITY_PAYLOADS: dict[CapabilityName, tuple[t.Any, t.Any]] = {
    CapabilityName.GET_AUTHORIZATION_URL: (GetAuthorizationUrlRequest, GetAuthorizationUrlResponse),
    CapabilityName.GET_LAST_ACTIVITY: (GetLastActivityRequest, GetLastActivityResponse),
    CapabilityName.HANDLE_AUTHORIZATION_CALLBACK: (
        HandleAuthorizationCallbackRequest,
        HandleAuthorizationCallbackResponse,
    ),
    CapabilityName.HANDLE_CLIENT_CREDENTIALS_REQUEST: (
        HandleClientCredentialsRequest,
        HandleClientCredentialsResponse,
    ),
    CapabilityName.LIST_ACCOUNTS: (ListAccountsRequest, ListAccountsResponse),
    CapabilityName.LIST_RESOURCES: (ListResourcesRequest, ListResourcesResponse),
    CapabilityName.LIST_ENTITLEMENTS: (ListEntitlementsRequest, ListEntitlementsResponse),
    CapabilityName.FIND_ENTITLEMENT_ASSOCIATIONS: (
        FindEntitlementAssociationsRequest,
        FindEntitlementAssociationsResponse,
    ),
    CapabilityName.LIST_CUSTOM_ATTRIBUTES_SCHEMA: (
        ListCustomAttributesSchemaRequest,
        ListCustomAttributesSchemaResponse,
    ),
    CapabilityName.REFRESH_ACCESS_TOKEN: (RefreshAccessTokenRequest, RefreshAccessTokenResponse),
    CapabilityName.CREATE_ACCOUNT: (CreateAccountRequest, CreateAccountResponse),
    CapabilityName.DELETE_ACCOUNT: (DeleteAccountRequest, DeleteAccountResponse),
    CapabilityName.ACTIVATE_ACCOUNT: (ActivateAccountRequest, ActivateAccountResponse),
    CapabilityName.DEACTIVATE_ACCOUNT: (DeactivateAccountRequest, DeactivateAccountResponse),
    CapabilityName.ASSIGN_ENTITLEMENT: (AssignEntitlementRequest, AssignEntitlementResponse),
    CapabilityName.UNASSIGN_ENTITLEMENT: (UnassignEntitlementRequest, UnassignEntitlementResponse),
    CapabilityName.VALIDATE_CREDENTIALS: (ValidateCredentialsRequest, ValidateCredentialsResponse),
}
