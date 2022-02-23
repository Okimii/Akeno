from __future__ import annotations

from typing import Any
from datetime import datetime

from .http import HTTPClient

__all__ = ("User",)


class User:
    """
    Represents a twitter user.

    params
    ------
    user_id: int` The id of the user.cd 
    """

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name, self.id

    @classmethod
    async def create(cls, user_id: int) -> User:
        """
        Creates a User object.

        params
        ------
        user_id: int` The user id.

        returns
        -------
        `User`
        """

        user = await HTTPClient().request(
            "GET",
            f"https://api.twitter.com/1.1/users/lookup.json?user_id={user_id}",
            headers={"Authorization": f"Bearer {HTTPClient().token}"},
        )
        cls.user: dict[int, dict[Any, Any]] = {}
        cls.user[1] = user
        return cls(user_id)

    @classmethod
    async def get_all_attrs_of(cls, user_id: int) -> dict[Any, Any]:
        """
        Creates a User object and returns all attributes.

        params
        ------
        user_id: int` The user id.

        returns
        -------
        dict`
        """

        user = await HTTPClient().request(
            "GET",
            f"https://api.twitter.com/1.1/users/lookup.json?user_id={user_id}",
            headers={"Authorization": f"Bearer {HTTPClient().token}"},
        )

        return cls(user_id), user

    @property
    def all_attrs(self) -> dict[int, dict[Any, Any]]:

        """
        All attributes for the user

        returns
        -------
        dict`
        """

        return self.user

    @property
    def id(self) -> int:

        """
        The user's id.

        returns
        -------
        `int`
        """

        return int(self.user[1][0]["id_str"])

    @property
    def name(self) -> str:

        """
        The user's name.

        returns
        -------
        `str`
        """

        return self.user[1][0]["name"]

    @property
    def handle(self) -> str:

        """
        The user's handle.

        returns
        -------
        dict`
        """

        return self.user[1][0]["screen_name"]

    @property
    def location(self) -> str:

        """
        The user's defined location.

        returns
        -------
        `str`
        """

        return self.user[1][0]["location"]

    @property
    def description(self) -> str:

        """
        The user's description.

        returns
        -------
        `str`
        """

        return self.user[1][0]["description"]

    @property
    def url(self) -> str:

        """
        User's defined url.

        returns
        -------
        `str`
        """

        return self.user[1][0]["url"]

    @property
    def protected(self) -> bool:

        """
        returns True if a user has chosen to protect their tweets.

        returns
        -------
        `bool`
        """

        return self.user[1][0]["protected"]

    @property
    def follower_count(self) -> int:

        """
        User's follower count.

        returns
        -------
        `int`
        """

        return self.user[1][0]["followers_count"]

    @property
    def following_count(self) -> int:

        """
        How many user's this account is following.

        returns
        -------
        `int`
        """

        return self.user[1][0]["friends_count"]

    @property
    def listed_count(self) -> int:

        """
        The number of of public lists that the user is a member of.

        returns
        -------
        `int`
        """

        return self.user[1][0]["listed_count"]

    @property
    def created_at(self) -> datetime:

        """
        The UTC datetime that the user account was created at.

        returns
        -------
        `datetime
        """

        return self.user[1][0]["created_at"]

    @property
    def favourite_count(self) -> int:

        """
        How many tweets the user has liked in the accounts lifetime.

        returns
        -------
        `int`
        """

        return self.user[1][0]["favourites_count"]

    @property
    def verified(self) -> bool:

        """
        Checks if the user is verified

        returns
        -------
        `bool`
        """

        return self.user[1][0]["verified"]

    @property
    def tweet_count(self) -> int:

        """
        How many tweets (including retweets) have been sent by the user.

        returns
        -------
        `int`
        """

        return self.user[1][0]["statuses_count"]

    @property
    def status(self) -> dict[Any, Any]:

        """
        Data about the user's status.

        returns
        -------
        dict`
        """

        return self.user[1][0]["status"]

    @property
    def avatar(self) -> str:

        """
        The user's profile image url.

        returns
        -------
        `str`
        """

        return self.user[1][0]["profile_image_url_https"]

    @property
    def banner(self) -> str:

        """
        The user's profile banner url.

        returns
        -------
        `str`
        """

        return self.user[1][0]["profile_banner_url"]
