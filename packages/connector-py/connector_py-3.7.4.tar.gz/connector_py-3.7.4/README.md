# Lumos Connectors

[![PyPI - Version](https://img.shields.io/pypi/v/connector-py.svg)](https://pypi.org/project/connector-py)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/connector-py.svg)](https://pypi.org/project/connector-py)

-----

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Error Handling](#error-handling)
- [OAuth Module](#oauth-module)
- [Scaffold](#scaffold)
- [Tips](#tips)
- [License](#license)

## Installation

```console
pip install connector-py
```

## Usage

The package can be used in three ways:

1. A CLI to scaffold a custom connector with its own CLI to call commands
2. A library to create a custom connector

To get started, run `connector --help`

An example of running a command that accepts arguments
in an integration connector called `mock-connector`:

```shell
mock-connector info
mock-connector validate_credentials --json '{"request":{},"auth":{}}'
```

### Connector implementation

Connectors can implement whichever Lumos capabilities make sense for the underlying app.

To see what a minimal implementation looks like, you can run

```sh
connector scaffold foo-bar projects/connectors/python/foo-bar
```

`projects/connectors/python/foo-bar/foo_bar/integration.py` will look something like this:

```python
integration = Integration(
    app_id="github",
    version=__version__,
    auth=BasicCredential,
    settings_model=FooBarSettings,
    exception_handlers=[
        (httpx.HTTPStatusError, HTTPHandler, None),
    ],
    description_data=DescriptionData(
        logo_url="https://logo.clearbit.com/foobar.com",
        user_friendly_name="Foo Bar",
        description="Foobar is a cloud-based platform that lets you manage foos and bars",
        categories=[AppCategory.DEVELOPERS, AppCategory.COLLABORATION],
    ),
    resource_types=resource_types,
    entitlement_types=entitlement_types,
)
```

Once an integration is created, you can register handlers for Lumos capabilities.

```py
@integration.register_capability(CapabilityName.LIST_ACCOUNTS)
async def list_accounts(request: ListAccountsRequest) -> ListAccountsResponse:
    # do whatever is needed to get accounts
    return ListAccountsResponse(
        response=[],
        raw_data=raw_data if request.include_raw_data else None,
        ...
    )
```

### Error Handling

Error handling is facilitated through an exception handler decorator.

An exception handler can be attached to the connector library as follows:

```python
from httpx import HTTPStatusError
from connector.oai.errors import HTTPHandler

integration = Integration(
    ...,
    exception_handlers=[
        (HTTPStatusError, HTTPHandler, None),
    ],
    handle_errors=True,
)
```

The decorator accepts a list of tuples of three. First tuple argument is the exception you would like to be catching, second is the handler (default or implemented on your own) and third is a specific error code that you would like to associate with this handler.

By default it is recommended to make use of the default HTTPHandler which will handle `raise_for_status()` for you and properly error code it. For more complex errors it is recommended to subclass the ExceptionHandler (in `connector/oai/errors.py`) and craft your own handler.

#### Raising an exception

Among this, there is a custom exception class available as well as a default list of error codes:

```python
from connector.oai.errors import ConnectorError
from connector.generated import ErrorCode

def some_method(self, args):
    raise ConnectorError(
        message="Received wrong data, x: y",
        app_error_code="foobar.some_unique_string",
        error_code=ErrorCode.BAD_REQUEST,
    )
```

It is preferred to raise any manually raisable exception with this class. A connector can implement its own error codes list, which should be properly documented.

### Response

Error codes are by default prefixed with the app_id of the connector that has raised the exception. In your implementation you don't need to worry about this and can only focus on the second and optionally third level of the error code.

An example response when handled this way:

```json
// BAD_REQUEST error from github connector
{"error":{"message":"Some message","status_code":400,"error_code":"github.bad_request","raised_by":"HTTPStatusError","raised_in":"github.sync_.lumos:validate_credentials"}, "response": null, "raw_data": null}
```

### OAuth Module

The OAuth module is responsible for handling the OAuth2.0 flow for a connector.
It is configured with `oauth_settings` in the `Integration` class.
Not configuring this object will disable the OAuth module completely.

```python
from connector.oai.modules.oauth_module_types import (
    OAuthSettings,
    OAuthCapabilities,
    OAuthRequest,
    RequestDataType,
)

integration = Integration(
    ...,
    oauth_settings=OAuthSettings(
        # Authorization & Token URLs for the particular connector
        authorization_url="https://app.connector.com/oauth/authorize",
        token_url="https://api.connector.com/oauth/v1/token",

        # Scopes per capability (space delimited string)
        scopes={
            CapabilityName.VALIDATE_CREDENTIALS: "test:scope another:scope",
            ... # further capabilities as implemented in the connector
        },

        # You can modify the request type if the default is not appropriate
        # common options for method are "POST" and "GET"
        # available options for data are "FORMDATA", "QUERY", and "JSON" (form-data / url query params / json body)
        # *default is POST and FORMDATA*
        request_type=OAuthRequest(data=RequestDataType.FORMDATA),

        # You can modify the authentication method if the default is not appropriate
        # available options for auth_method are "CLIENT_SECRET_POST" and "CLIENT_SECRET_BASIC"
        # *default is CLIENT_SECRET_POST*
        client_auth=ClientAuthenticationMethod.CLIENT_SECRET_POST,

        # You can turn off specific or all capabilities for the OAuth module
        # This means that these will either be skipped or you have to implement them manually
        capabilities=OAuthCapabilities(
            refresh_access_token=False,
        ),

        # You can specify the type of OAuth flow to use
        # Available options are "CODE_FLOW" and "CLIENT_CREDENTIALS"
        # *default is CODE_FLOW*
        flow_type=OAuthFlowType.CODE_FLOW,
    ),
)
```

It might happen that your integration requires a dynamic authorization/token URL.
For example when the service provider has specific URLs and uses the customers custom subdomain. (eg. `https://{subdomain}.service.com/oauth/authorize`)
In that case you can pass a callable that takes the request args (`AuthRequest`, without the auth parameter) as an argument (only available during request).

```python
# method definitions
def get_authorization_url(args: AuthRequest) -> str:
    settings = get_settings(args, ConnectorSettings)
    return f"https://{settings.subdomain}.service.com/oauth/authorize"

def get_token_url(args: AuthRequest) -> str:
    settings = get_settings(args, ConnectorSettings)
    return f"https://{settings.subdomain}.service.com/oauth/token"

# oauth settings
integration = Integration(
    ...,
    oauth_settings=OAuthSettings(
        authorization_url=get_authorization_url,
        token_url=get_token_url,
    ),
)
```

#### OAuth Flow Types

The OAuth module supports two flow types:
- `CODE_FLOW`: The authorization code flow (default)
- `CLIENT_CREDENTIALS`: The client credentials flow (sometimes called "2-legged OAuth" or "Machine-to-Machine OAuth")

The flow type can be specified in the `OAuthSettings` object.

Using the authorization code flow you have three available capabalities:
- `GET_AUTHORIZATION_URL`: To get the authorization URL
- `HANDLE_AUTHORIZATION_CALLBACK`: To handle the authorization callback
- `REFRESH_ACCESS_TOKEN`: To refresh the access token

Using the client credentials flow you have two available capabalities:
- `HANDLE_CLIENT_CREDENTIALS_REQUEST`: To handle the client credentials request, uses the token URL
- `REFRESH_ACCESS_TOKEN`: To refresh the access token

These are registered by default via the module and can be overriden by the connector.

If you run:

```sh
connector info
```

You will see that the OAuth capabilities are included in the available connector capabilities.

### Scaffold

To scaffold a custom connector, run `connector scaffold --help`

To scaffold the mock-connector, run
`connector scaffold mock-connector "projects/connectors/python/mock-connector"`

## Tips

#### The library I want to use is synchronous only

You can use a package called `asgiref`. This package converts I/O bound synchronous
calls into asyncio non-blocking calls. First, add asgiref to your dependencies list
in `pyproject.toml`. Then, in your async code, use `asgiref.sync_to_async` to convert
synchronous calls to asynchronous calls.

```python
from asgiref.sync import sync_to_async
import requests

async def async_get_data():
    response = await sync_to_async(requests.get)("url")
```

## License

`connector` is distributed under the terms of the [Apache 2.0](./LICENSE.txt) license.
