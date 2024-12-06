import contextvars
import logging
from contextlib import contextmanager
from typing import Any, Coroutine, Generator

import httpx
from gql.transport.httpx import HTTPXAsyncTransport as GqlHTTPXAsyncTransport
from urllib3.util.url import Url, parse_url

logger = logging.getLogger(__name__)


LUMOS_PROXY_URL: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "LUMOS_PROXY_URL", default=None
)
LUMOS_PROXY_HEADERS: contextvars.ContextVar[httpx.Headers] = contextvars.ContextVar(
    "LUMOS_PROXY_HEADERS", default=httpx.Headers()
)


@contextmanager
def proxy_settings(
    *, proxy_url: str | None, proxy_headers: dict[str, str] | httpx.Headers | None = None
) -> Generator[None, None, None]:
    """
    Set context to run some httpx requests that are rewritten to a proxy.

    Example:

      from httpx_rewrite import AsyncClient, proxy_settings

      with proxy_settings(proxy_url="https://mitm.lumos.com/whatever/path", proxy_headers={"password":"swordfish"}):
          client = AsyncClient()
          await client.get("https://a-real-url-to-call/different/path")
    """
    LUMOS_PROXY_URL.set(proxy_url)
    LUMOS_PROXY_HEADERS.set(httpx.Headers(proxy_headers))
    yield


def get_proxy_url() -> str | None:
    """Return the current URL requests should proxy to. Set this with proxy_settings()"""
    return LUMOS_PROXY_URL.get()


def get_proxy_headers() -> httpx.Headers:
    """Return the current headers that should be attached to proxied requests. Set this with proxy_settings()"""
    return LUMOS_PROXY_HEADERS.get()


class AsyncClient(httpx.AsyncClient):
    """
    A slightly modified version of httpx.AsyncClient, that may rewrite requests to go to a proxy.

    Requests will be rewritten when run within the proxy_settings() context.

    Rewritten requests...
    1. will go to the proxy URL
    2. will have the original request line (including fragment) preserved in the header `X-Forward-To`
    3. will have their headers preserved, EXCEPT FOR...
       a. `Host` will be set to the proxy host
       b. Additional headers will be set, and overwrite any passed-in headers, from
         - the LUMOS_PROXY_HEADERS environment variable (as JSON)
         - the accumulated calls to this module's `add_proxy_headers` function
    """

    def will_rewrite_request(self) -> bool:
        return bool(get_proxy_url())

    def send(self, request: httpx.Request, **kwargs) -> Coroutine[Any, Any, httpx.Response]:
        proxy_host = get_proxy_url()
        if proxy_host:
            logger.debug("Proxying all requests to %s", proxy_host)
            override = parse_url(proxy_host)
        else:
            return super(AsyncClient, self).send(request, **kwargs)

        # Update request URL
        url = str(request.url)
        updated = Url(
            scheme=override.scheme,
            host=override.host,
            port=override.port,
            path=override.path,
            query=override.query,
        )

        # Rewrite headers
        new_headers = request.headers.copy()
        new_headers["X-Forward-To"] = url
        new_headers["Host"] = Url(
            scheme=override.scheme, host=override.host, port=override.port
        ).url
        proxy_headers = get_proxy_headers()
        for header, value in proxy_headers.items():
            new_headers[header] = value

        # Get request body if applicable
        if request.method in ("POST", "PUT", "PATCH"):
            content = request.content or bytes([])
        else:
            content = None

        new_request = httpx.Request(
            method=request.method,
            url=updated.url,
            headers=new_headers,
            content=content,
        )

        return super(AsyncClient, self).send(new_request, **kwargs)


class HTTPXAsyncTransport(GqlHTTPXAsyncTransport):
    async def connect(self):
        # Call the superclass...
        await super().connect()

        # ... and then override its result
        self.client = AsyncClient(**self.kwargs)
