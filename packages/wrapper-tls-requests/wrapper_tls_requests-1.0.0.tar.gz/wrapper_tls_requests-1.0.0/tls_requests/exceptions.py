from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

__all__ = [
    "CookieConflictError",
    "HTTPError",
    "HTTPStatusError",
    "URLError",
    "RemoteProtocolError",
    "ProtocolError",
    "StreamConsumed",
    "StreamError",
    "TooManyRedirects",
    "TLSError",
]


class HTTPError(Exception):
    """HTTP Error"""

    def __init__(self, message: str) -> None:
        self.message = message


class ProtocolError(HTTPError):
    """Protocol Error"""


class RemoteProtocolError(HTTPError):
    """Remote Protocol Error"""


class TooManyRedirects(HTTPError):
    """Too Many Redirects."""


# Client errors
class TLSError(HTTPError):
    """TLS Error"""


class HTTPStatusError(HTTPError):
    """HTTP Status Error"""


class URLError(HTTPError):
    pass


class URLParamsError(URLError):
    pass


class CookieError(HTTPError):
    pass


class CookieConflictError(CookieError):
    pass


class StreamError(HTTPError):
    pass


class StreamConsumed(StreamError):
    pass


class StreamClosed(StreamError):
    pass
