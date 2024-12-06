from typing import Collection, Protocol


class TranslationProvider(Protocol):
    async def translate(self, strings: Collection[str]) -> dict[str, str]: ...


class IdentityTranslationProdiver(TranslationProvider):
    async def translate(self, strings: Collection[str]) -> dict[str, str]:
        return {string: string for string in strings}
