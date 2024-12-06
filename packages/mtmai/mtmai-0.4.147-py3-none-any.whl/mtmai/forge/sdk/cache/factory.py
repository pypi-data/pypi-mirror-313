from mtmai.forge.sdk.cache.base import BaseCache
from mtmai.forge.sdk.cache.local import LocalCache


class CacheFactory:
    __cache: BaseCache = LocalCache()

    @staticmethod
    def set_cache(cache: BaseCache) -> None:
        CacheFactory.__cache = cache

    @staticmethod
    def get_cache() -> BaseCache:
        return CacheFactory.__cache
