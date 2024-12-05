from typing import Optional


class GoogleBooksApiException(Exception):
    """General exception for EasyHttpRequest errors."""

    def __init__(self, message: str, original_exception: Optional[Exception] = None):
        super().__init__(message)
        self.original_exception = original_exception
