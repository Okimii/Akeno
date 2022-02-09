from typing import Any

__all__ = ("Cache",)


class Cache:
    """
    A cache class that has methods to access the clients cache.

    Parameters
    ----------
    obj: :class:`Any` object you're trying to cache or get.
    """

    def __init__(self):
        self.cache: dict[Any, dict[Any, Any]] = {}

    def save(self, key: Any, value: dict[Any, Any]) -> None:
        """
        saves the given key and value to cache.

        Parameters
        ----------
        key: :class:`int` key of the value you want to store.
        value: :class:`dict` value that you're trying to cache
        """
        self.cache[key] = value

    def get(self, key: int) -> dict[Any, Any]:
        """
        gets a value with a key from cache.

        Parameters
        ----------
        key: :class:`int` key of the value you want to get.

        Returns
        -------
        :class:`dict`
        """
        return self.cache[key]

    def all_cache_items(self) -> dict[Any, dict[Any, Any]]:
        """
        gets all values and keys from cache.

        Returns
        -------
        :class:`dict`
        """
        return self.cache

    def get_index(self, key: int, index0: str, index1: str) -> str:
        """
        gets a string with a key from cache.

        Parameters
        ----------
        key: :class:`int` key of the value you want to get.
        index0: :class:`str` first index.
        index1: :class:`str` second index.

        Returns
        -------
        :class:`str`
        """
        return self.cache[key][index0][index1]
