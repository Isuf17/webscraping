from dependency_injector import resources
import httpx


class HttpxClient(resources.AsyncResource):
    def __init__(self, timeout: float):
        super().__init__()
        self._timeout = timeout

    async def init(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(timeout=self._timeout)

    async def shutdown(self, client: httpx.AsyncClient):
        await client.aclose()
