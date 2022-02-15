from typing import Any

__all__ = ("Cache",)


class Cache:
    def __init__(self):
        self.cache: dict[Any, dict[Any, Any]] = {}

    def save(self, key: Any, value: dict[Any, Any]) -> None:
        self.cache[key] = value

    def get(self, key: int) -> dict[Any, Any]:
        return self.cache[key]

    def all_cache_items(self) -> dict[Any, dict[Any, Any]]:
        return self.cache

    def get_index(self, key: int, index0: str, index1: str) -> str:
        return self.cache[key][index0][index1]
