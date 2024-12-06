import typing as t
from enum import Enum

import pydantic

from connector.generated import CapabilityName
from connector.oai.capability import AuthRequest


class OAuthFlowType(str, Enum):
    CODE_FLOW = "CODE_FLOW"
    CLIENT_CREDENTIALS = "CLIENT_CREDENTIALS"


class ClientAuthenticationMethod(str, Enum):
    CLIENT_SECRET_POST = "CLIENT_SECRET_POST"
    CLIENT_SECRET_BASIC = "CLIENT_SECRET_BASIC"


class RequestMethod(str, Enum):
    GET = "GET"
    POST = "POST"


class RequestDataType(str, Enum):
    FORMDATA = "FORMDATA"
    JSON = "JSON"
    QUERY = "QUERY"


class OAuthRequest(pydantic.BaseModel):
    method: RequestMethod = RequestMethod.POST
    data: RequestDataType = RequestDataType.FORMDATA


class OAuthCapabilities(pydantic.BaseModel):
    get_authorization_url: bool | None = True
    handle_authorization_callback: bool | None = True
    handle_client_credentials_request: bool | None = True
    refresh_access_token: bool | None = True


class OAuthSettings(pydantic.BaseModel):
    authorization_url: str | t.Callable[[AuthRequest], str] | None = pydantic.Field(
        default=None,
        description="The URL to use to get the authorization code, if using the client credentials flow, this can be None. Can be a string, callable (method that accepts the request args and returns a string) or None.",
    )
    token_url: str | t.Callable[[AuthRequest], str] = pydantic.Field(
        description="The URL to use to get the access token, can be a string or callable (method that accepts the request args and returns a string).",
    )
    scopes: dict[CapabilityName, str] = pydantic.Field(
        default_factory=dict,
        description="A dictionary of scopes to request for the token, keyed by CapabilityName.",
    )
    flow_type: OAuthFlowType | None = pydantic.Field(
        default=OAuthFlowType.CODE_FLOW,
        description="The type of OAuth flow to use, defaults to CODE_FLOW.",
    )
    client_auth: ClientAuthenticationMethod | None = pydantic.Field(
        default=ClientAuthenticationMethod.CLIENT_SECRET_POST,
        description="The client authentication method to use, defaults to CLIENT_SECRET_POST.",
    )
    request_type: OAuthRequest | None = pydantic.Field(
        default=OAuthRequest(),
        description="The request type to use, defaults to POST with FORMDATA.",
    )
    capabilities: OAuthCapabilities | None = pydantic.Field(
        default=OAuthCapabilities(),
        description="The capabilities to use, defaults to all capabilities enabled.",
    )
