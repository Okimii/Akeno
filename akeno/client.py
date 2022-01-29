from aiohttp import ClientSession

import json

from ratelimit import(
    limits,
    sleep_and_retry
    )

class AkenoClient:
    def __init__(
        self,
        token: str
        ) -> None:
        self.token = token
        self.cache = {}
        self.headers = {
            "Authorization" : f"Bearer {self.token}"
        }

    @sleep_and_retry
    @limits(
        calls=900,
        period=900
        )
    async def fetch_tweet(
        self,
        tweet_id: int
        ) -> dict:
        async with ClientSession() as akeno:
            async with akeno.get(
                f"https://api.twitter.com/2/tweets/{tweet_id}",
                headers=self.headers
                ) as resp:
                dt = json.loads(await resp.text())
                self.cache[tweet_id] = dt
                return resp.status, dt
    
    @sleep_and_retry
    @limits(
        calls=900,
        period=900
        )
    async def fetch_tweets(
        self,
        *tweet_ids: tuple
        ) -> dict:
        async with ClientSession() as akeno:
            async with akeno.get(
                f"https://api.twitter.com/2/tweets/{','.join(tweet_ids)}",
                headers=self.headers
                ) as resp:
                dt = json.loads(await resp.text())
                return resp.status, dt

    
    async def get_tweet(
        self,
        tweet_id: int
        ) -> str:
        try:
            return self.cache[tweet_id]
        except KeyError:
            raise "Tweet has not been found in cache"
    
    @sleep_and_retry
    @limits(
        calls=900,
        period=900
        )
    async def getch_tweet(
        self,
        tweet_id: int
        ) -> dict:
        try:
            return self.cache[id]
        except KeyError:
            async with ClientSession() as akeno:
                async with akeno.get(
                    f"https://api.twitter.com/2/tweets/{tweet_id}",
                    headers=self.headers
                    ) as resp:
                    dt = json.loads(await resp.text())
                    self.cache[tweet_id] = dt
                    return resp.status, dt
    
    @sleep_and_retry
    @limits(
        calls=50,
        period=900
        )
    async def like_tweet(
        self,
        user_id: int,
        tweet_id: int
        ) -> dict:
        async with ClientSession() as akeno:
            async with akeno.post(
                f"https://api.twitter.com/2/users/{user_id}/likes",
                headers={
                    "Authorization" : f"Bearer {self.token}",
                    "Content-type" : " application/json",
                    "tweet_id" : f"{tweet_id}"
                    }

                ) as resp:
                dt = json.loads(await resp.text())
                self.cache[tweet_id] = dt
                return resp.status, dt
    @sleep_and_retry
    @limits(
        calls=50,
        period=900
        )
    async def unlike_tweet(
        self,
        user_id: int,
        tweet_id: int
        ) -> dict:
        async with ClientSession() as akeno:
            async with akeno.get(
                f"https://api.twitter.com/2/users/{user_id}/likes/{tweet_id}",
                headers=self.headers
                ) as resp:
                dt = json.loads(await resp.text())
                return resp.status, dt
    
