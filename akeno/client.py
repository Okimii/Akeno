from aiohttp import ClientSession

import asyncio

from typing import Any


class AkenoClient:
    def __init__(self, token: str) -> None:
        self.token = token
        self.cache: dict[int, dict[Any, Any]] = {}
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.lock = asyncio.Lock()


    async def close(self) -> None:
        await self.session.close()

    async def request(
        self, method: str, endpoint: str, headers: dict
    ) -> dict[Any, Any]:
        self.session = ClientSession(headers=headers)
        resp = await self.session.request(method, endpoint)
        try:
            if resp.headers["x-rate-limit-remaining"] == 1:
                await self.lock.acquire()
                await asyncio.sleep(900)
                self.lock.release()
        except KeyError:
            return await resp.json()
        return await resp.json()

    async def fetch_tweet(self, tweet_id: int) -> dict[Any, Any]:
        t = await self.request(
            "GET", f"https://api.twitter.com/2/tweets/{tweet_id}", headers=self.headers
        )
        self.cache[tweet_id] = t
        return t

    def get_tweet(self, tweet_id: int) -> None:
        try:
            self.cache[tweet_id]
        except KeyError:
            raise "No such tweet"

    async def getch_tweet(self, tweet_id: int) -> dict[Any, Any]:
        try:
            return self.cache[tweet_id]
        except KeyError:
            t = await self.request(
                "GET",
                f"https://api.twitter.com/2/tweets/{tweet_id}",
                headers=self.headers,
            )
            self.cache[tweet_id] = t
            return t

    async def fetch_tweets(self, *tweet_ids: int) -> dict[Any, Any]:
        t = await self.request(
            "GET",
            f"https://api.twitter.com/2/{','.join(tweet_ids)}",
            headers=self.headers,
        )
        self.cache[tweet_ids[0]] = t
        return t

    async def getch_tweets(self, *tweet_ids: int) -> dict[Any, Any]:
        try:
            return self.cache[tweet_ids[0]]
        except KeyError:
            t = await self.request(
                "GET",
                f"https://api.twitter.com/2/{','.join(tweet_ids)}",
                headers=self.headers,
            )
            self.cache[tweet_ids[0]] = t
            return t

    async def like_tweet(self, user_id: int, tweet_id: int) -> dict[Any, Any]:
        return await self.request(
            "POST",
            f"https://api.twitter.com/2/users/{user_id}/likes/",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-type": "application/json",
                "tweet_id": f"{tweet_id}",
            },
        )

    async def unlike_tweet(self, user_id: int, tweet_id: int) -> dict[Any, Any]:
        return await self.request(
            "DELETE",
            f"https://api.twitter.com/2/users/{user_id}/likes/{tweet_id}",
            headers=self.headers,
        )

    async def fetch_user(self, user_id: int) -> dict[Any, Any]:
        u = await self.request(
            "GET", f"https://api.twitter.com/2/users/{user_id}", headers=self.headers
        )
        self.cache[user_id] = u
        return u

    def get_user(self, user_id: int) -> None:
        try:
            self.cache[user_id]
        except KeyError:
            raise "No such user"

    async def getch_user(self, user_id: int) -> dict[Any, Any]:
        try:
            return self.cache[user_id]
        except KeyError:
            u = await self.request(
                "GET",
                f"https://api.twitter.com/2/users/{user_id}",
                headers=self.headers,
            )
            self.cache[user_id] = u
            return u

    async def fetch_user_profile_image(self, user_id: int) -> dict[Any, Any]:
        u = await self.request(
            "GET",
            f"https://api.twitter.com/2/users/{user_id}?user.fields=profile_image_url",
            headers=self.headers,
        )
        self.cache[user_id] = u
        return u["data"]["profile_image_url"]

    def get_user_profile_image(self, user_id: int) -> dict[Any, Any]:
        try:
            return self.cache[user_id]["data"]["profile_image_url"]
        except KeyError:
            raise "No such user profile image"

    async def getch_user_profile_image(self, user_id: int) -> dict[Any, Any]:
        try:
            return self.cache[user_id]["data"]["profile_image_url"]
        except KeyError:
            u = await self.request(
                "GET",
                f"https://api.twitter.com/2/users/{user_id}?user.fields=profile_image_url",
                headers=self.headers,
            )
            self.cache[user_id] = u
            return u["data"]["profile_image_url"]

    async def fetch_user_created_at(self, user_id: int) -> dict[Any, Any]:
        u = await self.request(
            "GET",
            f"https://api.twitter.com/2/users/{user_id}?user.fields=created_at",
            headers=self.headers,
        )
        self.cache[user_id] = u
        return u["data"]["created_at"]
