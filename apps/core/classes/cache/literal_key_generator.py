from apps.core.classes.cache.cache_key_generator import CacheKeyGeneratorMixin


class LiteralKeyGeneratorMixin(CacheKeyGeneratorMixin):
    SEPARATOR = ":"

    def __init__(self, separator: str | None = None):
        super().__init__(separator or self.SEPARATOR)
