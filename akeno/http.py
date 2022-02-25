from __future__ import annotations
import asyncio
from typing import Any

from aiohttp import ClientSession

__all__ = ("HTTPClient",)


class HTTPClient:
    def __init__(self) -> None:
        self.token = None
        self.lock = asyncio.Lock()
        self.headers = {"Authorization": f"Bearer {self.token}"}

    async def _request(
        self, method: str, endpoint: str, headers: dict[Any, Any]
    ) -> dict[Any, Any]:
        self.session = ClientSession(headers=headers)
        await self.lock.acquire()
        resp = await self.session.request(method, endpoint)
        if resp.headers.get("x-rate-limit-remaining") == 0:
            await asyncio.sleep(900)
            self.lock.release()
        elif resp.headers.get("x-rate-limit-remaining") is None:
            self.lock.release()
            await self.session.close()
            return await resp.json()
        await self.session.close()
        return await resp.json()
        
