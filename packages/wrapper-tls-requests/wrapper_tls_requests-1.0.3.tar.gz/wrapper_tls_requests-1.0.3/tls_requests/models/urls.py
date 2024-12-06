from __future__ import annotations

from abc import ABC
from collections.abc import Mapping
from typing import Any, ItemsView, KeysView, Union, ValuesView
from urllib.parse import ParseResult, quote, unquote, urlencode, urlparse

import idna

from ..exceptions import URLError, URLParamsError
from ..types import URL_ALLOWED_PARAMS, URLParamTypes

__all__ = ["URL", "URLParams", "Proxy"]


class URLParams(Mapping, ABC):
    def __init__(self, params: URLParamTypes = None, **kwargs):
        self._data = self._prepare(params, **kwargs)

    @property
    def params(self) -> str:
        return quote(str(self))

    def update(self, params: URLParamTypes = None, **kwargs):
        self._data.update(self._prepare(params, **kwargs))
        return self

    def keys(self) -> KeysView:
        return self._data.keys()

    def values(self) -> ValuesView:
        return self._data.values()

    def items(self) -> ItemsView:
        return self._data.items()

    def copy(self) -> URLParams:
        return self.__class__(self._data.copy())

    def __str__(self):
        return urlencode(self._data, doseq=True)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.items())

    def __contains__(self, key: Any) -> bool:
        return key in self._data

    def __setitem__(self, key, value):
        self._data.update(self._prepare({key: value}))

    def __getitem__(self, key):
        return self._data[key]

    def __delitem__(self, key):
        del self._data[key]

    def __iter__(self):
        return (k for k in self.keys())

    def __len__(self) -> int:
        return len(self._data)

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            if isinstance(other, Mapping):
                other = self.__class__(other)
            else:
                return False
        return bool(self.params == other.params)

    def _prepare(self, params: URLParamTypes = None, **kwargs) -> Mapping:
        params = params or {}
        if not isinstance(params, (dict, self.__class__)):
            raise URLParamsError("Invalid parameters.")

        params.update(kwargs)
        for k, v in params.items():
            if not isinstance(k, (str, bytes)):
                raise URLParamsError("Invalid parameters key type.")

            if isinstance(v, (list, tuple, set)):
                v = [self.normalize(s) for s in v]
            else:
                v = self.normalize(v)

            params[self.normalize(k)] = v
        return params

    def normalize(self, s: URL_ALLOWED_PARAMS):
        if not isinstance(s, URL_ALLOWED_PARAMS):
            raise URLParamsError("Invalid parameters value type.")

        if isinstance(s, bool):
            return str(s).lower()

        if isinstance(s, bytes):
            return s.decode("utf-8")

        return str(s)


class URL:
    def __init__(self, url: Union[str, bytes], params: URLParamTypes = None, **kwargs):
        self._url = self._prepare(url, params)
        self._params = URLParams(params)
        self._parsed = None
        self._auth = None
        self._fragment = None
        self._host = None
        self._path = None
        self._netloc = None
        self._password = None
        self._port = None
        self._query = None
        self._scheme = None
        self._username = None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = self._prepare(value)

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, value):
        self._params = URLParams(value)

    @property
    def parsed(self) -> ParseResult:
        if self._parsed is None:
            self._parsed = urlparse(self.url)
        return self._parsed

    @property
    def auth(self) -> Union[tuple, None]:
        if self._auth is None:
            if self.parsed.username or self.parsed.password:
                self._auth = self.parsed.username, self.parsed.password
            else:
                self._auth = None, None
        return self._auth

    @property
    def fragment(self) -> str:
        if self._fragment is None:
            self._fragment = self.parsed.fragment
        return self._fragment

    @property
    def host(self) -> str:
        if self._host is None:
            try:
                self._host = idna.encode(self.parsed.hostname.lower()).decode("ascii")
            except AttributeError:
                self._host = ""
            except idna.IDNAError:
                raise URLError("Invalid IDNA hostname.")
        return self._host

    @property
    def path(self):
        if self._path is None:
            self._path = self.parsed.path
        return self._path

    @property
    def netloc(self) -> str:
        return ":".join([self.host, self.port]) if self.port else self.host

    @property
    def password(self) -> str:
        if self._password is None:
            self._password = self.parsed.password or ""
        return self._password

    @property
    def port(self) -> str:
        if self._port is None:
            port = ""
            try:
                if self.parsed.port:
                    port = str(self.parsed.port)
            except ValueError as e:
                raise URLError("%s. port range must be 0 - 65535." % e.args[0])

            self._port = port
        return self._port

    @property
    def query(self) -> str:
        if self._query is None:
            self._query = ""
            if self.parsed.query and self.params.params:
                self._query = "&".join([quote(self.parsed.query), self.params.params])
            elif self.params.params:
                self._query = self.params.params
            elif self.parsed.query:
                self._query = self.parsed.query
        return self._query

    @property
    def scheme(self) -> str:
        if self._scheme is None:
            self._scheme = self.parsed.scheme
        return self._scheme

    @property
    def username(self) -> str:
        if self._username is None:
            self._username = self.parsed.username or ""
        return self._username

    def __str__(self):
        return self._build()

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, unquote(self._build(True)))

    def _prepare(self, url: Union["URL", str, bytes], params: URLParamTypes) -> str:
        try:
            if isinstance(url, self.__class__):
                return self._prepare(str(url), params)

            if url:
                url = (
                    value.decode("utf-8").lstrip()
                    if isinstance(url, bytes)
                    else url.lstrip()
                )
                return url

        except Exception as e:
            raise URLError("Invalid URL, details: %s" % e)

        raise URLError("Not found URL.")

    def _build(self, secure: bool = False) -> str:
        urls = [self.scheme, "://"]
        authority = self.netloc
        if self.username or self.password:
            authority = "@".join(
                [
                    ":".join([self.username, "[secure]" if self.password else ""]),
                    self.netloc,
                ]
            )

        urls.append(authority)
        if self.query:
            urls.append("?".join([self.path, self.query]))
        else:
            urls.append(self.path)

        if self.fragment:
            urls.append("#".join([self.fragment]))

        return "".join(urls)


class Proxy(URL):
    ALLOWED_SCHEMES = ("http", "https", "socks5", "socks5h")

    @property
    def scheme(self) -> str:
        if self._scheme is None:
            if str(self.parsed.scheme).lower() not in self.ALLOWED_SCHEMES:
                raise ValueError("Invalid scheme.")

            self._scheme = self.parsed.scheme

        return self._scheme
