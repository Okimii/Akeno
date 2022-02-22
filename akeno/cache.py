from typing import Any, Optional

__all__ = ("Cache",)


class Cache:
    def __init__(self):
        self.cache: dict[Any, dict[Any, Any]] = {}

    def __dict__(self) -> dict[Any, Any]:
        return self.cache

    def __len__(self) -> int:
        return len(self.cache)

    def save(self, key: Any, value: dict[Any, Any]) -> None:
        self.cache[key] = value

    def get(self, key: int) -> Optional[dict[Any, Any]]:
        return self.cache.get(key)

    @property
    def items(self) -> Optional[dict[Any, dict[Any, Any]]]:
        return self.cache

    def get_index(self, key: int, index0: str, index1: str) -> Optional[str]:
        try:
            return self.cache[key][index0][index1]
        except KeyError:
            return None
