from aiohttp import ClientSession

import asyncio

from typing import Any


class AkenoClient:
    def __init__(self, token: str) -> None:
        self.token = token
        self.cache: dict[int, dict[Any, Any]] = {}
        self.headers = {"Authorization" : f"Bearer {self.token}"}
        self.lock = asyncio.Lock()
     
    async def __aenter__(self) -> "AkenoClient":
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.close()
    
    async def close(self) -> None:
        await self.session.close()

    async def request(self, method: str, endpoint: str, headers: dict) -> dict[Any, Any]:
        self.session = ClientSession(headers=headers)
        resp = await self.session.request(method, endpoint)
        try:
            if resp.headers["x-rate-limit-remaining"] == 1:
                await self.lock.acquire()
                asyncio.sleep(900)
                self.lock.release()
        except KeyError:
            return await resp.json()
        return await resp.json()

    async def fetch_tweet(self, tweet_id: int) -> dict[Any, Any]:
        t = await self.request("GET", f"https://api.twitter.com/2/tweets/{tweet_id}", headers=self.headers)
        self.cache[tweet_id] = t
        return t
    
    def get_tweet(self, tweet_id: int) -> dict[Any, Any]:
        try:
            return self.cache[tweet_id]
        except KeyError:
            raise "No such tweet"
    
    async def fetch_tweets(self, *tweet_ids: int) -> dict[Any, Any]:
        t = await self.request("GET", f"https://api.twitter.com/2/{','.join(tweet_ids)}", headers=self.headers)
        self.cache[tweet_ids[0]] = t
        return t
