from dependency_injector import containers, providers
from webscraping.common.clients.httpx_client.httpx_client import HttpxClient
from webscraping.common.clients.gemini_client.gemini_client import GeminiClient
from webscraping.common.clients.gemini_client.igemini_client import IGeminiClient
from webscraping.common.config import Settings


class Container(containers.DeclarativeContainer):
    config = providers.Singleton(Settings)

    httpx_client = providers.Resource(
        HttpxClient,
        timeout=10.0,
    )

    gemini_client = providers.Singleton(
        IGeminiClient.register(GeminiClient),
        api_key=config.provided.gemini_api_key,
        client=httpx_client,
    )
