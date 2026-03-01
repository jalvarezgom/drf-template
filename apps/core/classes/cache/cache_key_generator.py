class CacheKeyGeneratorMixin:
    SEPARATOR = ":"

    def __init__(self, separator: str | None = None):
        if separator is not None:
            self.__class__.SEPARATOR = separator
