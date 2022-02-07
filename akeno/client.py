import asyncio
from typing import Any

from aiohttp import ClientSession

__all__ = ("AkenoClient",)


class AkenoClient:
    """
    A client class that has methods to access the twitter API.
    Parameters
    ----------
    token: :class:`str` Bare token used for authorization
    """

    def __init__(self, token: str) -> None:
        self.token = token
        self.cache: dict[int, dict[Any, Any]] = {}
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.lock = asyncio.Lock()

    async def __aenter__(self) -> "AkenoClient":
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.close()

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
            await self.session.close()
            return await resp.json()
        await self.session.close()
        return await resp.json()

    async def fetch_tweet(self, tweet_id: int) -> dict[Any, Any]:
        """
        Makes a request to the api to get a tweet.
        Parameters
        ----------
        tweet_id: :class:`int` id of the tweet you're trying to fetch.
        Returns
        -------
        :class:`dict`
        """

        tweet = await self.request(
            "GET", f"https://api.twitter.com/2/tweets/{tweet_id}", headers=self.headers
        )
        self.cache[tweet_id] = tweet
        return tweet

    def get_tweet(self, tweet_id: int) -> dict[Any, Any]:
        """
        Gets the tweet by id from cache.
        Parameters
        ----------
        tweet_id: :class:`int` id of the tweet you're trying to get.
        Returns
        -------
        :class:`dict`
        """
        return self.cache[tweet_id]

    async def getch_tweet(self, tweet_id: int) -> dict[Any, Any]:
        """
        Tries to get the tweet by id from cache, if it fails it will make a request to the api.
        Parameters
        ----------
        tweet_id: :class:`int` id of the tweet you're trying to get or fetch.
        Returns
        -------
        :class:`dict`
        """

        try:
            return self.cache[tweet_id]
        except KeyError:
            tweet = await self.request(
                "GET",
                f"https://api.twitter.com/2/tweets/{tweet_id}",
                headers=self.headers,
            )
            self.cache[tweet_id] = tweet
            return tweet

    async def fetch_tweets(self, *tweet_ids: str) -> dict[Any, Any]:
        """
        Makes a request to the api to get tweets.
        Parameters
        ----------
        tweet_ids: :class:`str` ids of the tweet you're trying to fetch.
        Returns
        -------
        :class:`dict`
        """
        tweets = await self.request(
            "GET",
            f"https://api.twitter.com/2/{','.join(tweet_ids)}",
            headers=self.headers,
        )
        self.cache[tweet_ids] = tweets
        return tweets

    async def getch_tweets(self, *tweet_ids: str) -> dict[Any, Any]:
        """
        Tries to get the tweets by id from cache, if it fails it will make a request to the api.
        Parameters
        ----------
        tweet_ids: :class:`int` ids of the tweets you're trying to get or fetch.
        Returns
        -------
        :class:`dict`
        """
        try:
            return self.cache[int(tweet_ids[0])]
        except KeyError:
            tweets = await self.request(
                "GET",
                f"https://api.twitter.com/2/{','.join(tweet_ids)}",
                headers=self.headers,
            )
            self.cache[tweet_ids] = tweets
            return tweets

    async def like_tweet(self, user_id: int, tweet_id: int) -> dict[Any, Any]:
        """
        Likes a tweet for a user.
        Parameters
        ----------
        user_id: :class:`int` your own id to like the given tweet.
        tweet_id: :class:`int` id of the tweets you're trying to like.

        Returns
        -------
        :class:`dict`
        """
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
        """
        Unlikes a tweet for a user.
        Parameters
        ----------
        user_id: :class:`int` your own id to like the given tweet.
        tweet_id: :class:`int` id of the tweets you're trying to like.

        Returns
        -------
        :class:`dict`
        """
        return await self.request(
            "DELETE",
            f"https://api.twitter.com/2/users/{user_id}/likes/{tweet_id}",
            headers=self.headers,
        )

    async def fetch_user(self, user_id: int) -> dict[Any, Any]:
        """
        Makes a request to the api to get a user.
        Parameters
        ----------
        user_id: :class:`int` id of the user you're trying to fetch.

        Returns
        -------
        :class:`dict`
        """
        user = await self.request(
            "GET", f"https://api.twitter.com/2/users/{user_id}", headers=self.headers
        )
        self.cache[user_id] = user
        return user

    def get_user(self, user_id: int) -> dict[Any, Any]:
        """
        Gets the user by id from cache.
        Parameters
        ----------
        user_id: :class:`int` id of the user you're trying to get.

        Returns
        -------
        :class:`dict`
        """
        return self.cache[user_id]

    async def getch_user(self, user_id: int) -> dict[Any, Any]:
        """
        Tries to get the user by id from cache, if it fails it will make a request to the api.
        Parameters
        ----------
        user_id :class:`int` id of the user you're trying to get or fetch.

        Returns
        -------
        :class:`dict`
        """
        try:
            return self.cache[user_id]
        except KeyError:
            user = await self.request(
                "GET",
                f"https://api.twitter.com/2/users/{user_id}",
                headers=self.headers,
            )
            self.cache[user_id] = user
            return user

    async def fetch_user_profile_image(self, user_id: int) -> str:
        """
        Makes a request to the api to get a users profile picture as a url.
        Parameters
        ----------
        user_id: :class:`int` id of the user you're trying to fetch.

        Returns
        -------
        :class:`str`
        """
        user = await self.request(
            "GET",
            f"https://api.twitter.com/2/users/{user_id}?user.fields=profile_image_url",
            headers=self.headers,
        )
        self.cache[user_id] = user
        return user["data"]["profile_image_url"]

    def get_user_profile_image(self, user_id: int) -> str:
        """
        Gets the users profile picture as a url by id from cache.
        Parameters
        ----------
        user_id: :class:`int` id of the user you're trying to get.

        Returns
        -------
        :class:`str`
        """
        return self.cache[user_id]["data"]["profile_image_url"]

    async def getch_user_profile_image(self, user_id: int) -> str:
        """
        Tries to get the user profile image by id from cache, if it fails it will make a request to the api.
        Parameters
        ----------
        user_id: :class:`int` id of the user you're trying to get or fetch.

        Returns
        -------
        :class:`str`
        """
        try:
            return self.cache[user_id]["data"]["profile_image_url"]
        except KeyError:
            user = await self.request(
                "GET",
                f"https://api.twitter.com/2/users/{user_id}?user.fields=profile_image_url",
                headers=self.headers,
            )
            self.cache[user_id] = user
            return user["data"]["profile_image_url"]

    async def fetch_user_created_at(self, user_id: int) -> str:
        """
        Makes a request to the api to get a users date of the account creation.
        Parameters
        ----------
        user_id: :class:`int` id of the user you're trying to fetch.

        Returns
        -------
        :class:`str`
        """
        user = await self.request(
            "GET",
            f"https://api.twitter.com/2/users/{user_id}?user.fields=created_at",
            headers=self.headers,
        )
        self.cache[user_id] = user
        return user["data"]["created_at"]

    def get_user_created_at(self, user_id: int) -> str:
        """
        Gets the users date of account creation by id from cache.
        Parameters
        ----------
        user_id: :class:`int` id of the user you're trying to get.

        Returns
        -------
        :class:`str`
        """
        return self.cache[user_id]["data"]["created_at"]

    async def getch_user_created_at(self, user_id: int) -> str:
        """
        Tries to get the users date of account creation, if it fails it will make a request to the api.
        Parameters
        ----------
        user_id: :class:`int` id of the user you're trying to get or fetch.

        Returns
        -------
        :class:`str`
        """
        try:
            return self.cache[user_id]["data"]["created_at"]
        except KeyError:
            user = await self.request(
                "GET",
                f"https://api.twitter.com/2/users/{user_id}?user.fields=created_at",
                headers=self.headers,
            )
            self.cache[user_id] = user
            return user["data"]["created_at"]

    async def fetch_user_metrics(self, user_id: int) -> dict[Any, Any]:
        """
        Makes a request to the api to get the metrics of a user.
        Parameters
        ----------
        user_id: :class:`int` id of the user you're trying to fetch.

        Returns
        -------
        :class:`dict`
        """
        user = await self.request(
            "GET",
            f"https://api.twitter.com/2/users/{user_id}?user.fields=public_metrics",
            headers=self.headers,
        )
        self.cache[user_id] = user
        return user["data"]["public_metrics"]

    def get_user_metrics(self, user_id: int) -> dict[Any, Any]:
        """
        Gets the users metrics by id from cache.
        Parameters
        ----------
        user_id: :class:`int` id of the user you're trying to get.

        Returns
        -------
        :class:`dict`
        """
        return self.cache[user_id]["data"]["public_metrics"]

    async def getch_user_metrics(self, user_id: int) -> dict[Any, Any]:
        """
        Tries to get the metrics of a user from cache, if it fails it will make a request to the api.
        Parameters
        ----------
        user_id: :class:`int` id of the user you're trying to get or fetch.
        Returns
        -------
        :class:`dict`
        """
        try:
            return self.cache[user_id]["data"]["public_metrics"]
        except KeyError:
            user = await self.request(
                "GET",
                f"https://api.twitter.com/2/users/{user_id}?user.fields=public_metrics",
                headers=self.headers,
            )
            self.cache[user_id] = user
            return user["data"]["public_metrics"]
