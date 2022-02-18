from typing import Any

from httpclient import HTTPClient
from cache import Cache


__all__ = ("AkenoClient",)


class AkenoClient(HTTPClient, Cache):
    """
    A main client class.

    Parameters
    ----------
    token: :class:`str` Bearer token used for authorization
    """

    def __init__(self, token: str) -> None:
        self.token = token
        HTTPClient.__init__(self)
        Cache.__init__(self)
        setattr(HTTPClient, "token", token)

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
        self.save(tweet_id, tweet)
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
        return self.get(tweet_id)

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
            return self.get(tweet_id)
        except KeyError:
            tweet = await self.request(
                "GET",
                f"https://api.twitter.com/2/tweets/{tweet_id}",
                headers=self.headers,
            )
            self.save(tweet_id, tweet)
            return tweet

    async def fetch_tweets(self, *tweet_ids: int) -> dict[Any, Any]:
        """
        Makes a request to the api to get the tweets.

        Parameters
        ----------
        tweet_ids: :class:`int` ids of the tweet you're trying to fetch.

        Returns
        -------
        :class:`dict`
        """
        tweets = await self.request(
            "GET",
            f"https://api.twitter.com/2/tweets?ids={','.join(list(map(str, [i for i in tweet_ids])))}",
            headers=self.headers,
        )
        self.save(tweet_ids, tweets)
        return tweets

    async def getch_tweets(self, *tweet_ids: int) -> dict[Any, Any]:
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
            return self.get(tweet_ids)
        except KeyError:
            tweets = await self.request(
                "GET",
                f"https://api.twitter.com/2/tweets?ids={','.join(list(map(str, [i for i in tweet_ids])))}",
                headers=self.headers,
            )
            self.save(tweet_ids, tweets)
            return tweets

    def get_tweets(self, *tweet_ids: int) -> dict[Any, Any]:
        """
        Gets the tweet by id from cache.

        Parameters
        ----------
        tweet_ids: :class:`int` ids of the tweet you're trying to get.

        Returns
        -------
        :class:`dict`
        """
        return self.get(tweet_ids)

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

        self.save(user_id, user)
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
        return self.get(user_id)

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
            return self.get(user_id)
        except KeyError:
            user = await self.request(
                "GET",
                f"https://api.twitter.com/2/users/{user_id}",
                headers=self.headers,
            )
            self.save(user_id, user)
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
        self.save(user_id, user)
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
        return self.get_index(user_id, "data", "profile_image_url")

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
            return self.get_index(user_id, "data", "profile_image_url")
        except KeyError:
            user = await self.request(
                "GET",
                f"https://api.twitter.com/2/users/{user_id}?user.fields=profile_image_url",
                headers=self.headers,
            )
            self.save(user_id, user)
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
        self.save(user_id, user)
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
        return self.get_index(user_id, "data", "created_at")

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
            return self.get_index(user_id, "data", "created_at")
        except KeyError:
            user = await self.request(
                "GET",
                f"https://api.twitter.com/2/users/{user_id}?user.fields=created_at",
                headers=self.headers,
            )
            self.save(user_id, user)
            return user["data"]["created_at"]

    async def fetch_user_metrics(self, user_id: int) -> str:
        """
        Makes a request to the api to get the metrics of a user.

        Parameters
        ----------
        user_id: :class:`int` id of the user you're trying to fetch.

        Returns
        -------
        :class:`str`
        """
        user = await self.request(
            "GET",
            f"https://api.twitter.com/2/users/{user_id}?user.fields=public_metrics",
            headers=self.headers,
        )

        return user["data"]["public_metrics"]

    def get_user_metrics(self, user_id: int) -> str:
        """
        Gets the users metrics by id from cache.

        Parameters
        ----------
        user_id: :class:`int` id of the user you're trying to get.

        Returns
        -------
        :class:`str`
        """
        return self.get_index(user_id, "data", "public_metrics")

    async def getch_user_metrics(self, user_id: int) -> str:
        """
        Tries to get the metrics of a user from cache, if it fails it will make a request to the api.

        Parameters
        ----------
        user_id: :class:`int` id of the user you're trying to get or fetch.

        Returns
        -------
        :class:`str`
        """
        try:
            return self.get_index(user_id, "data", "public_metrics")
        except KeyError:
            user = await self.request(
                "GET",
                f"https://api.twitter.com/2/users/{user_id}?user.fields=public_metrics",
                headers=self.headers,
            )
            self.save(user_id, user)
            return user["data"]["public_metrics"]

    async def retweet(self, user_id: int, tweet_id: int) -> dict[Any, Any]:
        """
        Makes a request to the api to retweet the given tweet.

        Parameters
        ----------
        user_id: :class:`int` your'e own id to retweet the given tweet.
        tweet_id: :class:`int` tweet you're trying to retweet.

        Returns
        -------
        :class:`dict`
        """
        return await self.request(
            "POST",
            f"https://api.twitter.com/2/users/{user_id}/retweets",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-type": "application/json",
                "tweet_id": f"{tweet_id}",
            },
        )

    async def post_tweet(self, text: str) -> dict[Any, Any]:
        """
        Makes a request to the api to post a tweet.

        Parameters
        ----------
        text: :class:`str` the text of the tweet you will post.

        Returns
        -------
        :class:`dict`
        """

        return await self.request(
            "POST",
            f"https://api.twitter.com/2/tweets",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-type": "application/json",
                "text": text,
            },
        )

    async def delete_tweet(self, tweet_id: int) -> dict[Any, Any]:
        """
        Makes a request to the api to delete a tweet.

        Parameters
        ----------
        tweet_id: :class:`int` the tweet id of the tweet you want to delete.

        Returns
        -------
        :class:`dict`
        """

        return await self.request(
            "DELETE",
            f"https://api.twitter.com/2/tweets/{tweet_id}",
            headers=self.headers,
        )

    async def fetch_tweet_created_at(self, tweet_id: int) -> str:
        """
        Makes a request to the api to get when the tweet was created.

        Parameters
        ----------
        tweet_id: :class:`int` id of the tweet you're trying to fetch.

        Returns
        -------
        :class:`str`
        """
        tweet = await self.request(
            "GET",
            f"https://api.twitter.com/2/tweets/{tweet_id}?tweet.fields=created_at",
            headers=self.headers,
        )
        self.save(tweet_id, tweet)
        return tweet["data"]["created_at"]

    def get_tweet_created_at(self, tweet_id: int) -> str:
        """
        Gets when the tweet was created from cache.

        Parameters
        ----------
        tweet_id: :class:`int` id of the user you're trying to get.

        Returns
        -------
        :class:`str`
        """
        return self.get_index(tweet_id, "data", "created_at")

    async def getch_tweet_created_at(self, tweet_id: int) -> str:
        """
        Tries to get the tweet date of creation, if it fails it will make a request to the api.

        Parameters
        ----------
        tweet_id: :class:`int` id of the user you're trying to get or fetch.

        Returns
        -------
        :class:`str`
        """
        try:
            return self.get_index(tweet_id, "data", "created_at")
        except KeyError:
            tweet = await self.request(
                "GET",
                f"https://api.twitter.com/2/tweets/{tweet_id}?user.fields=created_at",
                headers=self.headers,
            )
            self.save(tweet_id, tweet)
            return tweet["data"]["created_at"]

    async def fetch_tweet_metrics(self, tweet_id: int) -> str:
        """
        Makes a request to the api to get the metrics of a tweet.

        Parameters
        ----------
        tweet_id: :class:`int` id of the tweet you're trying to fetch.

        Returns
        -------
        :class:`str`
        """
        tweet = await self.request(
            "GET",
            f"https://api.twitter.com/2/tweets/{tweet_id}?tweet.fields=public_metrics",
            headers=self.headers,
        )
        self.save(tweet_id, tweet)
        return tweet["data"]["public_metrics"]

    def get_tweet_metrics(self, tweet_id: int) -> str:
        """
        Gets the tweet metrics by id from cache.

        Parameters
        ----------
        tweet_id: :class:`int` id of the tweet you're trying to get.

        Returns
        -------
        :class:`str`
        """
        return self.get_index(tweet_id, "data", "public_metrics")

    async def getch_tweet_metrics(self, tweet_id: int) -> str:
        """
        Tries to get the metrics of a tweet from cache, if it fails it will make a request to the api.

        Parameters
        ----------
        tweet_id: :class:`int` id of the tweet you're trying to get or fetch.

        Returns
        -------
        :class:`str`
        """
        try:
            return self.get_index(tweet_id, "data", "public_metrics")
        except KeyError:
            tweet = await self.request(
                "GET",
                f"https://api.twitter.com/2/tweets/{tweet_id}?tweet.fields=public_metrics",
                headers=self.headers,
            )
            self.save(tweet_id, tweet)
            return tweet["data"]["public_metrics"]

    async def fetch_tweet_source(self, tweet_id: int) -> str:
        """
        Makes a request to the api to get the source of a tweet.

        Parameters
        ----------
        tweet_id: :class:`int` id of the tweet you're trying to fetch.

        Returns
        -------
        :class:`str`
        """
        tweet = await self.request(
            "GET",
            f"https://api.twitter.com/2/tweets/{tweet_id}?tweet.fields=source",
            headers=self.headers,
        )
        self.save(tweet_id, tweet)
        return tweet["data"]["source"]

    def get_tweet_source(self, tweet_id: int) -> str:
        """
        Gets the tweet source by id from cache.

        Parameters
        ----------
        tweet_id: :class:`int` id of the tweet you're trying to get.

        Returns
        -------
        :class:`str`
        """
        return self.get_index(tweet_id, "data", "source")

    async def getch_tweet_source(self, tweet_id: int) -> str:
        """
        Tries to get the source  of a tweet from cache, if it fails it will make a request to the api.

        Parameters
        ----------
        tweet_id: :class:`int` id of the tweet you're trying to get or fetch.

        Returns
        -------
        :class:`str`
        """
        try:
            return self.get_index(tweet_id, "data", "source")
        except KeyError:
            tweet = await self.request(
                "GET",
                f"https://api.twitter.com/2/tweets/{tweet_id}?tweet.fields=source",
                headers=self.headers,
            )
            self.save(tweet_id, tweet)
            return tweet["data"]["source"]
