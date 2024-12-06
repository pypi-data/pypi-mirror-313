from typing import Collection, Protocol


class CacheProvider(Protocol):
    async def get(self, strings: Collection[str]) -> dict[str, str]: ...

    async def set(self, strings: dict[str, str]) -> None: ...


class NullCacheProvider(CacheProvider):
    async def get(self, strings: Collection[str]) -> dict[str, str]:
        return {}

    async def set(self, strings: dict[str, str]) -> None:
        pass
