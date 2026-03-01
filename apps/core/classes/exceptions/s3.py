class S3Exception(Exception):
    """Base exception class."""

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def message(self):
        return f"[S3] Exception: {self}"

    def __repr__(self):
        return self.message
