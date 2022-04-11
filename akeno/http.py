from __future__ import annotations

import asyncio

from aiohttp import ClientSession
from typing import Any


__all__ = ("HTTPClient",)


class HTTPClient:
    def __init__(self, token: str) -> None:
        self.token = token
        self.lock = asyncio.Lock()

    async def request(
        self, method: str, endpoint: str, headers: dict[Any, Any]
    ) -> dict[Any, Any]:
        """
        Makes a request to the endpoint
        with the method and headers.

        Returns
        -------
        :class:`dict[Any, Any]`
            The json returned from the call.
        """

        self.session = ClientSession(headers=headers)
        await self.lock.acquire()

        async with self.session.request(method, endpoint) as response:
            if response.headers.get("x-rate-limit-remaining") == 0:
                await asyncio.sleep(900)
                self.lock.release()
            elif response.headers.get("x-rate-limit-remaining") is None:
                self.lock.release()
                await self.session.close()
                return await response.json()
            return await response.json()
