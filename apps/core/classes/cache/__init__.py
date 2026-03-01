from apps.core.classes.cache.cache_system import CacheSystemMixin
from apps.core.classes.cache.literal_key_generator import LiteralKeyGeneratorMixin


class Cache(CacheSystemMixin):
    # class Actions(CacheGetterMixin, CacheSetterMixin, CacheDeleterMixin):
    #     pass

    class KeyGenerator(LiteralKeyGeneratorMixin):
        pass
