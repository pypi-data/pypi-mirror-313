import httpx
from connector.generated import (
    ActivateAccountRequest,
    ActivateAccountResponse,
    AssignEntitlementRequest,
    AssignEntitlementResponse,
    CreateAccountRequest,
    CreateAccountResponse,
    DeactivateAccountRequest,
    DeactivateAccountResponse,
    DeleteAccountRequest,
    DeleteAccountResponse,
    FindEntitlementAssociationsRequest,
    FindEntitlementAssociationsResponse,
    FoundAccountData,
    GetLastActivityRequest,
    GetLastActivityResponse,
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
    UnassignEntitlementRequest,
    UnassignEntitlementResponse,
    ValidateCredentialsRequest,
    ValidateCredentialsResponse,
    ValidatedCredentials,
)
from connector.httpx_rewrite import AsyncClient
from connector.oai.capability import CapabilityName, Request, get_oauth, get_page
from connector.oai.errors import HTTPHandler
from connector.oai.integration import DescriptionData, Integration
from connector.utils.httpx_auth import BearerAuth

from {name}.__about__ import __version__
from {name}.enums import entitlement_types, resource_types
from {name}.serializers.pagination import DEFAULT_PAGE_SIZE, NextPageToken, Pagination
from {name}.settings import {pascal}Settings

BASE_URL = "https://{hyphenated_name}.com"


def build_client(request: Request) -> AsyncClient:
    """Prepare client context manager for calling {title} API."""
    return AsyncClient(
        auth=BearerAuth(token=get_oauth(request).access_token),
        base_url=BASE_URL,
    )


integration = Integration(
    app_id="{hyphenated_name}",
    version=__version__,
    auth=OAuthCredential,
    exception_handlers=[
        (httpx.HTTPStatusError, HTTPHandler, None),
    ],
    description_data=DescriptionData(
        logo_url="", user_friendly_name="{pascal}", description="", categories=[]
    ),
    settings_model={pascal}Settings,
    resource_types=resource_types,
    entitlement_types=entitlement_types,
)


@integration.register_capability(CapabilityName.VALIDATE_CREDENTIALS)
async def validate_credentials(
    args: ValidateCredentialsRequest,
) -> ValidateCredentialsResponse:
    async with build_client(args) as client:
        r = await client.get("/users", params={{"limit": 1}})
        r.raise_for_status()

    return ValidateCredentialsResponse(
        response=ValidatedCredentials(
            unique_tenant_id="REPLACE_WITH_UNIQUE_TENANT_ID",
            valid=True,
        ),
    )


@integration.register_capability(CapabilityName.LIST_ACCOUNTS)
async def list_accounts(args: ListAccountsRequest) -> ListAccountsResponse:
    endpoint = "/users"
    try:
        current_pagination = NextPageToken(get_page(args).token).paginations()[0]
    except IndexError:
        current_pagination = Pagination.default(endpoint)

    page_size = get_page(args).size or DEFAULT_PAGE_SIZE
    async with build_client(args) as client:
        r = await client.get(
            endpoint,
            params={{"limit": page_size, "offset": current_pagination.offset}},
        )
        r.raise_for_status()
        accounts: list[FoundAccountData] = []

        next_pagination = []
        if True:
            next_pagination.append(
                Pagination(
                    endpoint=endpoint,
                    offset=current_pagination.offset + len(accounts),
                )
            )

        next_page_token = NextPageToken.from_paginations(next_pagination).token

    return ListAccountsResponse(
        response=accounts,
        page=Page(
            token=next_page_token,
            size=page_size,
        )
        if next_page_token
        else None,
    )


# @integration.register_capability(CapabilityName.LIST_RESOURCES)
async def list_resources(args: ListResourcesRequest) -> ListResourcesResponse:
    raise NotImplementedError


# @integration.register_capability(CapabilityName.LIST_ENTITLEMENTS)
async def list_entitlements(
    args: ListEntitlementsRequest,
) -> ListEntitlementsResponse:
    raise NotImplementedError


# @integration.register_capability(CapabilityName.FIND_ENTITLEMENT_ASSOCIATIONS)
async def find_entitlement_associations(
    args: FindEntitlementAssociationsRequest,
) -> FindEntitlementAssociationsResponse:
    raise NotImplementedError


#@integration.register_capability(CapabilityName.GET_LAST_ACTIVITY)
async def get_last_activity(args: GetLastActivityRequest) -> GetLastActivityResponse:
    raise NotImplementedError


# @integration.register_capability(CapabilityName.ASSIGN_ENTITLEMENT)
async def assign_entitlement(args: AssignEntitlementRequest) -> AssignEntitlementResponse:
    raise NotImplementedError


# @integration.register_capability(CapabilityName.UNASSIGN_ENTITLEMENT)
async def unassign_entitlement(
    args: UnassignEntitlementRequest,
) -> UnassignEntitlementResponse:
    raise NotImplementedError


# @integration.register_capability(CapabilityName.LIST_CUSTOM_ATTRIBUTES_SCHEMA)
async def list_custom_attributes_schema(
    args: ListCustomAttributesSchemaRequest,
) -> ListCustomAttributesSchemaResponse:
    raise NotImplementedError


# @integration.register_capability(CapabilityName.CREATE_ACCOUNT)
async def create_account(
    args: CreateAccountRequest,
) -> CreateAccountResponse:
    raise NotImplementedError


# @integration.register_capability(CapabilityName.DELETE_ACCOUNT)
async def delete_account(
    args: DeleteAccountRequest,
) -> DeleteAccountResponse:
    raise NotImplementedError


# @integration.register_capability(CapabilityName.ACTIVATE_ACCOUNT)
async def activate_account(
    args: ActivateAccountRequest,
) -> ActivateAccountResponse:
    raise NotImplementedError


# @integration.register_capability(CapabilityName.DEACTIVATE_ACCOUNT)
async def deactivate_account(
    args: DeactivateAccountRequest,
) -> DeactivateAccountResponse:
    raise NotImplementedError
