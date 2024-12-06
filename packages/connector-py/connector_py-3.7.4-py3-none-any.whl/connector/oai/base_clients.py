from abc import abstractmethod

from connector.httpx_rewrite import AsyncClient
from connector.oai.capability import Request


class BaseIntegrationClient:
    @classmethod
    @abstractmethod
    def prepare_client_args(cls, args: Request) -> dict:
        pass

    @classmethod
    def build_client(cls, args) -> AsyncClient:
        return AsyncClient(**cls.prepare_client_args(args))

    def __init__(self, args: Request) -> None:
        self._http_client = self.build_client(args)

    async def __aenter__(self):
        await self._http_client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._http_client.__aexit__()
        if exc_type is not None:
            raise exc_val
