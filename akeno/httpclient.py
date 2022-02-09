from aiohttp import ClientSession

from typing import Any

import asyncio

__all__ = ("HttpClient",)


class HttpClient:
    """
    A httpclient class that has methods to access the twitter API.

    Parameters
    ----------
    token: :class:`str` Bare token used for authorization.
    """

    def __init__(self, token: str) -> None:
        self.token = token
        self.lock = asyncio.Lock()
        self.headers = {"Authorization": f"Bearer {self.token}"}

    async def __aenter__(self) -> "HttpClient":
        """
        Enter for context managers.
        """
        return self

    async def __aexit__(self, *_: Any) -> None:
        """
        Exit for context managers.
        """
        await self.close()

    async def close(self) -> None:
        """
        Close the clientsession.
        """
        await self.session.close()

    async def request(
        self, method: str, endpoint: str, headers: dict
    ) -> dict[Any, Any]:
        """
        A request method to access the twitter API.

        Parameters
        ----------
        method: :class:`str` the request method.
        endpoint: :class:`str` the endpoint url.
        headers: :class:`dict` the request headers.

        Returns
        -------
        :class:`dict`
        """
        self.session = ClientSession(headers=headers)
        resp = await self.session.request(method, endpoint)
        try:
            if resp.headers["x-rate-limit-remaining"] == 1:
                await self.lock.acquire()
                await asyncio.sleep(900)
                self.lock.release()
        except KeyError:
            await self.session.close()
            return await resp.json()
        await self.session.close()
        return await resp.json()
