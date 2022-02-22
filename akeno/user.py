from datetime import datetime
from typing import Any

from .http import HTTPClient

__all__ = ("User",)


class User:
    """
    Represents a twitter user.
    
    Parameters
    ----------
    user_id: :class:`int` The id of the user.
    """

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name, self.id

    @classmethod
    async def create(cls, user_id: int) -> "User":
        """
        Creates a User object.
        
        Parameters
        ----------
        user_id: :class:`int` The user id.
        
        Returns
        -------
        :class:`User`
        """
        user = await HTTPClient().request(
            "GET", f"https://api.twitter.com/1.1/users/lookup.json?user_id={user_id}",
            headers={"Authorization": f"Bearer {HTTPClient().token}"}
        )
        cls.user: dict[int, dict[Any, Any]] = {}
        cls.user[1] = user
        return cls(user_id)

    @property
    def all_attrs(self) -> dict[int, dict[Any, Any]]:
        """
        Returns all attributes for the user
        
        Returns
        -------
        :class:`dict`
        """
        return self.user

    @property
    def id(self) -> int:
        """
        Returns the user's id.
        
        Returns
        -------
        :class:`int`
        """
        return int(self.user[1][0]["id_str"])

    @property
    def name(self) -> str:
        """
        Returns the user's name.
        
        Returns
        -------
        :class:`str`
        """
        return self.user[1][0]["name"]

    @property
    def handle(self) -> str:
        """
        Returns the user's handle.
        
        Returns
        -------
        :class:`dict`
        """
        return self.user[1][0]["screen_name"]

    @property
    def location(self) -> str:
        """
        Returns the user's defined location.
        
        Returns
        -------
        :class:`str`
        """
        return self.user[1][0]["location"]

    @property
    def description(self) -> str:
        """
        Returns the user's description.
        
        Returns
        -------
        :class:`str`
        """
        return self.user[1][0]["description"]

    @property
    def url(self) -> str:
        """
        Returns the user's defined url.
        
        Returns
        -------
        :class:`str`
        """
        return self.user[1][0]["url"]

    @property
    def protected(self) -> bool:
        """
        Returns True if a user has chosen to protect their tweets.
        
        Returns
        -------
        :class:`bool`
        """
        return self.user[1][0]["protected"]

    @property
    def follower_count(self) -> int:
        """
        Returns a user's follower count.
        
        Returns
        -------
        :class:`int`
        """
        return self.user[1][0]["followers_count"]

    @property
    def following_count(self) -> int:
        """
        Returns how many user's this account is following.
        
        Returns
        -------
        :class:`int`
        """
        return self.user[1][0]["friends_count"]

    @property
    def listed_count(self) -> int:
        """
        Returns the number of of public lists that the user is a member of.
        
        Returns
        -------
        :class:`int`
        """
        return self.user[1][0]["listed_count"]

    @property
    def created_at(self) -> datetime:
        """
        Returns the UTC datetime that the user account was created at.
        
        Returns
        -------
        :class:`datetime`
        """
        return self.user[1][0]["created_at"]

    @property
    def favourite_count(self) -> int:
        """
        Returns how many tweets the user has liked in the accounts lifetime.
        
        Returns
        -------
        :class:`int`
        """
        return self.user[1][0]["favourites_count"]

    @property
    def verified(self) -> bool:
        """
        Returns True if a user is verified.
        
        Returns
        -------
        :class:`bool`
        """
        return self.user[1][0]["verified"]

    @property
    def tweet_count(self) -> int:
        """
        Returns how many tweets (including retweets) have been sent by the user.
        
        Returns
        -------
        :class:`int`
        """
        return self.user[1][0]["statuses_count"]

    @property
    def status(self) -> dict[Any, Any]:
        """
        Returns data about the user's status.
        
        Returns
        -------
        :class:`dict`
        """
        return self.user[1][0]["status"]

    @property
    def avatar(self) -> str:
        """
        Returns the user's profile image url.
        
        Returns
        -------
        :class:`str`
        """
        return self.user[1][0]["profile_image_url_https"]

    @property
    def banner(self) -> str:
        """
        Returns the user's profile banner url.
        
        Returns
        -------
        :class:`str`
        """
        return self.user[1][0]["profile_banner_url"]
