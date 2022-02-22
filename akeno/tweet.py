from http import HTTPClient
from typing import Any
from datetime import datetime

__all__(
    "Tweet",
)


class Tweet:
    """
    Represents a twitter tweet.

    Parameters
    ----------
    tweet_id: :class:`int` the id of the tweet.

    """

    def __init__(self, tweet_id: int) -> None:
        self.id = tweet_id

    @classmethod
    async def create(cls, tweet_id: int) -> "Tweet":
        """
        Creates a Tweet object.

        Parameters
        ----------
        tweet_id: :class:`int` The tweet id.

        Returns
        -------
        :class:`Tweet`
        """
        tweet = await HTTPClient().request(
            "GET",
            f"https://api.twitter.com/1.1/statuses/show.json?id={tweet_id}",
            headers={"Authorization": f"Bearer {HTTPClient().token}"},
        )
        cls.tweet: dict[int, dict[Any, Any]] = {}
        cls.tweet[1] = tweet
        return cls(tweet_id)

    @classmethod
    async def get_all_attrs_of(tweet_id: int) -> dict[Any, Any]:
        """
        Creates a Tweet object and returns all attributes as raw json.

        Parameters
        ----------
        tweet_id: :class:`int` The tweet id.

        Returns
        -------
        :class:`Tweet`
        """
        tweet = await HTTPClient().request(
            "GET",
            f"https://api.twitter.com/1.1/statuses/show.json?id={tweet_id}",
            headers={"Authorization": f"Bearer {HTTPClient().token}"},
        )
        return cls(tweet_id), tweet

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return self.text, self.str_id

    @property
    def all_attrs(self) -> dict[int, dict[Any, Any]]:
        """
        Returns all attributes for the tweet.

        Returns
        -------
        :class:`dict`
        """
        return self.tweet

    @property
    def created_at(self) -> datetime:
        """
        Returns the UTC datetime when the user account was created at.

        Returns
        -------
        :class:`datetime`
        """
        return self.tweet[1]["created_at"]

    @property
    def author_profile_image(self) -> str:
        """
        Returns the author's profile image as a url.

        Returns
        -------
        :class:`str`
        """
        return self.tweet[1]["user"]["profile_image_url"]

    @property
    def id(self) -> int:
        """
        Returns the tweet's id.

        Returns
        -------
        :class:`int`
        """
        return self.tweet[1]["id"]

    @property
    def text(self) -> str:
        """
        Returns the tweet's text.

        Returns
        -------
        :class:`str`
        """
        return self.tweet[1]["text"]

    @property
    def str_id(self) -> str:
        """
        Returns the tweet's id as a str.

        Returns
        -------
        :class:`str`
        """
        return self.tweet[1]["id_str"]

    @property
    def hastags(self) -> list[str]:
        """
        Returns the a list of hashtags in a tweet.

        Returns
        -------
        :class:`list`
        """
        return self.tweet[1]["entities"]["hashtags"]

    @property
    def user_mentions(self) -> list[str]:
        """
        Returns the a list of user mentions in a tweet.

        Returns
        -------
        :class:`list`
        """
        return self.tweet[1]["entities"]["user_mentions"]

    @property
    def urls(self) -> list[str]:
        """
        Returns the a list of urls in a tweet.

        Returns
        -------
        :class:`list`
        """
        return self.tweet[1]["entities"]["urls"]

    @property
    def symbols(self) -> list[str]:
        """
        Returns the a list of symbols in a tweet.

        Returns
        -------
        :class:`list`
        """
        return self.tweet[1]["entities"]["symbols"]

    @property
    def source(self) -> str:
        """
        Returns the source of where a tweet was sent.

        Returns
        -------
        :class:`str`
        """
        return self.tweet[1]["source"]

    @property
    def author_id(self) -> int:
        """
        Returns the author's id.

        Returns
        -------
        :class:`int`
        """
        return self.tweet[1]["user"]["id"]

    @property
    def author_str_id(self) -> str:
        """
        Returns the author's id as a str.

        Returns
        -------
        :class:`str`
        """
        return self.tweet[1]["user"]["id_str"]

    @property
    def author_name(self) -> str:
        """
        Returns the author's name.

        Returns
        -------
        :class:`str`
        """
        return self.tweet[1]["user"]["name"]

    @property
    def author_handle(self) -> str:
        """
        Returns the author's handle.

        Returns
        -------
        :class:`str`
        """
        return self.tweet[1]["user"]["screen_name"]

    @property
    def author_location(self) -> str:
        """
        Returns the author's location.

        Returns
        -------
        :class:`str`
        """
        return self.tweet[1]["user"]["location"]

    @property
    def author_bio(self) -> str:
        """
        Returns the author's bio or description.

        Returns
        -------
        :class:`str`
        """
        return self.tweet[1]["user"]["description"]

    @property
    def author_bio_urls(self) -> list[str]:
        """
        Returns a list of the urls in the author's bio or description.

        Returns
        -------
        :class:`list`
        """
        return self.tweet[1]["user"]["entities"]["description"]["urls"]

    @property
    def author_protected(self) -> bool:
        """
        Returns if the author is protected.

        Returns
        -------
        :class:`bool`
        """
        return self.tweet[1]["user"]["protected"]

    @property
    def author_followers_count(self) -> int:
        """
        Returns the author's followers count.

        Returns
        -------
        :class:`int`
        """
        return self.tweet[1]["user"]["followers_count"]

    @property
    def author_friends_count(self) -> int:
        """
        Returns the author's friends count.

        Returns
        -------
        :class:`int`
        """
        return self.tweet[1]["user"]["friends_count"]

    @property
    def author_listed_count(self) -> int:
        """
        Returns the author's listed count.

        Returns
        -------
        :class:`int`
        """
        return self.tweet[1]["user"]["listed_count"]

    @property
    def author_created_at(self) -> datetime:
        """
        Returns the UTC datetime when the author account was created at.

        Returns
        -------
        :class:`datetime`
        """
        return self.tweet[1]["user"]["created_at"]

    @property
    def author_favourites_count(self) -> int:
        """
        Returns the author's favourites count.

        Returns
        -------
        :class:`int`
        """
        return self.tweet[1]["user"]["favourites_count"]

    @property
    def author_geo_enabled(self) -> bool:
        """
        Returns if the author's geo is enabled.

        Returns
        -------
        :class:`bool`
        """
        return self.tweet[1]["user"]["geo_enabled"]

    @property
    def author_is_verified(self) -> bool:
        """
        Returns if the author is verified.

        Returns
        -------
        :class:`bool`
        """
        return self.tweet[1]["user"]["verified"]

    @property
    def author_profile_background_color(self) -> str:
        """
        Returns the author's profile background color.

        Returns
        -------
        :class:`str`
        """
        return self.tweet[1]["user"]["profile_background_color"]

    @property
    def author_profile_background_image_url(self) -> str:
        """
        Returns the author's profile background image url.

        Returns
        -------
        :class:`str`
        """
        return self.tweet[1]["user"]["profile_background_image_url"]

    @property
    def author_profile_image_url(self) -> str:
        """
        Returns the author's profile image url.

        Returns
        -------
        :class:`str`
        """
        return self.tweet[1]["user"]["profile_image_url"]

    @property
    def author_retweet_count(self) -> int:
        """
        Returns the author's retweet count.

        Returns
        -------
        :class:`int`
        """
        return self.tweet[1]["user"]["retweet_count"]