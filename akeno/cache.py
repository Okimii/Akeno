from typing import Any

__all__ = ("Cache",)


class Cache:
    def __init__(self):
        self.cache: dict[Any, dict[Any, Any]] = {}

    
    def __dict__(self) -> dict[Any, Any]:
        return self.cache

    def __len__(self) -> int:
        return len(self.cache)

    def _save(self, key: Any, value: dict[Any, Any]) -> None:
        self.cache[key] = value

    def _get(self, key: int) -> None | dict[Any, Any]:
        try:
            return self.cache[key]
        except KeyError:
            return None

    @property
    def all_cache_items(self) -> None | dict[Any, Any]:
        return self.cache

    def _get_index(self, key: int, index: str) -> None | str:
        try:
            return self.cache[key][index0][index1]
        except KeyError:
            return None
