from __future__ import annotations
from typing import Any
from .user import User
from .tweet import Tweet
from .http import HTTPClient

__all__ = ("AkenoClient",)


class AkenoClient(HTTPClient):

    """
    A main client class.

    Parameters
    ----------
    token: :class:`str` Barer token used for authorization
    """

    def __init__(self, token: str, client_user_id: int) -> None:
        self.token = token
        self.user_id = client_user_id
        HTTPClient.__init__(self)
        setattr(HTTPClient, "token", token)

    async def fetch_tweet(self, tweet_id: int) -> Tweet:

        """
        Makes a request to the api to get a tweet.

        Parameters
        ----------
        tweet_id: :class:`int` id of the tweet you're trying to fetch.

        Returns
        -------
        :class:`Tweet`
        """

        return await Tweet.create(tweet_id)

    async def like_tweet(self, tweet_id: int) -> dict[Any, Any]:

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
        return await self._request(
            "POST",
            f"https://api.twitter.com/2/users/{self.user_id}/likes/",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-type": "application/json",
                "tweet_id": tweet_id,
            },
        )

    async def unlike_tweet(self, tweet_id: int) -> dict[Any, Any]:

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
        return await self._request(
            "DELETE",
            f"https://api.twitter.com/2/users/{self.user_id}/likes/{tweet_id}",
            headers=self.headers,
        )

    async def fetch_user(self, user_id: int) -> User:

        """
        Makes a request to the api to get a user.

        Parameters
        ----------
        user_id: :class:`int` id of the user you're trying to fetch.

        Returns
        -------
        :class:`User`
        """
        return await User.create(user_id)

    async def retweet(self, tweet_id: int) -> dict[Any, Any]:

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
        return await self._request(
            "POST",
            f"https://api.twitter.com/2/users/{self.user_id}/retweets",
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

        return await self._request(
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

        return await self._request(
            "DELETE",
            f"https://api.twitter.com/2/tweets/{tweet_id}",
            headers=self.headers,
        )
