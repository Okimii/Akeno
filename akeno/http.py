import asyncio
from aiohttp import ClientSession

from typing import Any


__all__ = ("HTTPClient",)


class HTTPClient:
    def __init__(self) -> None:
        self.lock = asyncio.Lock()
        self.headers = {"Authorization": f"Bearer {self.token}"}

    async def _request(
        self, method: str, endpoint: str, headers: dict[Any, Any]
    ) -> dict[Any, Any]:
        self.session = ClientSession(headers=headers)
        try:
            await self.lock.acquire()
            resp = await self.session.request(method, endpoint)
            if resp.headers["x-rate-limit-remaining"] == 0:
                await asyncio.sleep(900)
                self.lock.release()
            self.lock.release()
        except KeyError:
            await self.session.close()
            return await resp.json()
        await self.session.close()
        return await resp.json()
