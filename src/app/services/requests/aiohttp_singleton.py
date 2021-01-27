"""Module contains class for async requests"""
import aiohttp
import logging
from socket import AF_INET

logger = logging.getLogger(__name__)


SIZE_POOL_AIOHTTP: int = 100


class SingletonAiohttp:
    aiohttp_client: aiohttp.ClientSession = None

    @classmethod
    def get_aiohttp_client(cls, auth=None) -> aiohttp.ClientSession:
        if cls.aiohttp_client is None:
            timeout = aiohttp.ClientTimeout(total=2)
            connector = aiohttp.TCPConnector(
                family=AF_INET, limit_per_host=SIZE_POOL_AIOHTTP
            )
            cls.aiohttp_client = aiohttp.ClientSession(
                timeout=timeout, connector=connector, auth=auth
            )

        return cls.aiohttp_client

    @classmethod
    async def close_aiohttp_client(cls):
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    @classmethod
    async def get(cls, url: str):
        client = cls.get_aiohttp_client()
        async with client.get(url) as response:
            content = response.content
        return content
