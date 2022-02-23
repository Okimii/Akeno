import typing as t

from .user import User
from .tweet import Tweet
from .http import HTTPClient

__all__ = ("AkenoClient",)


class AkenoClient(HTTPClient):
    """
    Represents the AkenoClient
    which handles all interactions
    and classes.

    params
    ------
    `token: str`
        Bearer token used for to
        authorize the client user.
    """

    def __init__(self, token: str) -> None:
        self.token = token
        HTTPClient.__init__(self)
        setattr(HTTPClient, "token", token)

    async def fetch_user(self, user_id: int) -> t.Optional[User]:
        """
        Attempts to fetch a user
        from the api.

        params
        ------
        `user_id: int`
            id of the user attempting
            to be fetched.

        returns
        -------
        `user: User`
            the user returned if
            found, else None.
        """

        user = await User.create(user_id)
        return user or None

    async def fetch_tweet(self, tweet_id: int) -> t.Optional[Tweet]:
        """
        Makes a request to the api to fetch
        a tweet with `tweet_id`.

        params
        ------
        `tweet_id: int`
            id of the tweet attempting
            to be fetched.

        returns
        -------
        `tweet: t.Optional[Tweet]`
            the tweet that was returned
            if it was found, else None.
        """

        tweet = await Tweet.create(tweet_id)
        return tweet or None

    async def like_tweet(self, user_id: int, tweet_id: int) -> dict[t.Any, t.Any]:
        """
        Likes a tweet from a user
        with a user id of `user_id`
        and the tweet with an id of
        `tweet_id`.

        params
        ------
        `user_id: int`
            the user id to like the given tweet.
        `tweet_id: int`
            id of the tweets you're trying to like.

        returns
        -------
        `dict`
            the response returned when
            attempting to like the tweet.
        """

        return await self._request(
            "POST",
            f"https://api.twitter.com/2/users/{user_id}/likes/",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-type": "application/json",
                "tweet_id": f"{tweet_id}",
            },
        )

    async def unlike_tweet(self, user_id: int, tweet_id: int) -> dict[t.Any, t.Any]:
        """
        Removes a likes froma tweet
        with id `tweet_id` and removes
        the like from a user with
        a user id of `user_id`.

        params
        ------
        `user_id: int`
            the user id to unlike the
            tweet.
        `tweet_id: int`
            id of the tweets attempting
            to be unliked.

        returns
        -------
        `dict`
            the response returned when
            attempting to unlike the tweet.
        """

        return await self._request(
            "DELETE", f"https://api.twitter.com/2/users/{user_id}/likes/{tweet_id}", headers=self.headers
        )

    async def retweet(self, user_id: int, tweet_id: int) -> dict[t.Any, t.Any]:
        """
        A user with user id `user_id`
        attempting to retweet a tweet
        with id of `tweet_id`.

        params
        ------
        `user_id: int`
            the user id to retweet the given tweet.
        `tweet_id: int`
            tweet is attempting to retweet.

        returns
        -------
        `dict`
            the response returned when
            attempting to retweet the tweet.
        """

        return await self._request(
            "POST",
            f"https://api.twitter.com/2/users/{user_id}/retweets",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-type": "application/json",
                "tweet_id": f"{tweet_id}",
            },
        )

    async def post_tweet(self, text: str) -> dict[t.Any, t.Any]:
        """
        Attempts to post a tweet
        with a text of `text`.

        params
        ------
        `text: str`
            the text of the tweet you will post.

        returns
        -------
        `dict`
            the response returned when
            attempting to retweet the tweet.
        """

        return await self._request(
            "POST",
            f"https://api.twitter.com/2/tweets",
            headers={"Authorization": f"Bearer {self.token}", "Content-type": "application/json", "text": text},
        )

    async def delete_tweet(self, tweet_id: int) -> dict[t.Any, t.Any]:
        """
        Deletes a tweet with an
        id of `tweet_id`.

        params
        ------
        `tweet_id: int`
            the tweet id of the tweet
            attempting to be deleted.

        returns
        -------
        `dict`
            the response returned when
            attempting to delete the tweet.
        """

        return await self._request("DELETE", f"https://api.twitter.com/2/tweets/{tweet_id}", headers=self.headers)
