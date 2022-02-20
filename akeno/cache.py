from typing import Any, Optional

__all__ = ("Cache",)


class Cache:
    def __init__(self):
        self.cache: dict[Any, dict[Any, Any]] = {}

    def _save(self, key: Any, value: dict[Any, Any]) -> None:
        self.cache[key] = value

    def _get(self, key: int) -> Optional[dict[Any, Any]]:
        try:
            return self.cache[key]
        except KeyError:
            return None

    @property
    def all_cache_items(self) -> Optional[dict[Any, dict[Any, Any]]]:
        return self.cache

    def _get_index(self, key: int, index: str) -> Optional[str]:
        try:
            return self.cache[key][index0][index1]
        except KeyError:
            return None
