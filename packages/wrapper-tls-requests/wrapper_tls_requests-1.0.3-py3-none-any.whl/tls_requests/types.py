"""
Type definitions for type checking purposes.
"""

from http.cookiejar import CookieJar
from typing import (IO, TYPE_CHECKING, Any, BinaryIO, Callable, List, Literal,
                    Mapping, Optional, Sequence, Tuple, TypeAlias, Union)
from uuid import UUID

if TYPE_CHECKING:  # pragma: no cover
    from .models import Cookies, Headers, Request  # noqa: F401

AuthTypes = Optional[
    Union[
        Tuple[Union[str, bytes], Union[str, bytes]],
        Callable,
        "Auth",
        "BasicAuth",
    ]
]
URLTypes = Union["URL", str]
URL_ALLOWED_PARAMS = Union[str, bytes, int, float, bool]
URLParamTypes = Optional[
    Union[
        "URLParams",
        Mapping[
            Union[str, bytes],
            Union[
                URL_ALLOWED_PARAMS,
                list[URL_ALLOWED_PARAMS],
                tuple[URL_ALLOWED_PARAMS],
                set[URL_ALLOWED_PARAMS],
            ],
        ],
    ]
]
MethodTypes = Union[
    "Method", Literal["GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"]
]
ProtocolTypes = Optional[Union[Literal["auto", "http1", "http2"], bool]]
HookTypes = Optional[Mapping[Literal["request", "response"], Sequence[Callable]]]
TLSSession = Union["TLSSession", None]
TLSSessionId = Union[str, UUID]
TLSPayload = Union[dict, str, bytes, bytearray]
TLSCookiesTypes = Optional[List[dict[str, str]]]
TLSIdentifierTypes: TypeAlias = Literal[
    "chrome_103",
    "chrome_104",
    "chrome_105",
    "chrome_106",
    "chrome_107",
    "chrome_108",
    "chrome_109",
    "chrome_110",
    "chrome_111",
    "chrome_112",
    "chrome_116_PSK",
    "chrome_116_PSK_PQ",
    "chrome_117",
    "chrome_120",
    "chrome_124",
    "safari_15_6_1",
    "safari_16_0",
    "safari_ios_15_5",
    "safari_ios_15_6",
    "safari_ios_16_0",
    "firefox_102",
    "firefox_104",
    "firefox_105",
    "firefox_106",
    "firefox_108",
    "firefox_110",
    "firefox_117",
    "firefox_120",
    "opera_89",
    "opera_90",
    "opera_91",
    "okhttp4_android_7",
    "okhttp4_android_8",
    "okhttp4_android_9",
    "okhttp4_android_10",
    "okhttp4_android_11",
    "okhttp4_android_12",
    "okhttp4_android_13",
    "zalando_ios_mobile",
    "zalando_android_mobile",
    "nike_ios_mobile",
    "nike_android_mobile",
    "mms_ios",
    "mms_ios_2",
    "mms_ios_3",
    "mesh_ios",
    "mesh_ios_2",
    "mesh_android",
    "mesh_android_2",
    "confirmed_ios",
    "confirmed_android",
    "confirmed_android_2",
]

HeaderTypes = Optional[
    Union[
        "Headers",
        Mapping[str, str],
        Mapping[bytes, bytes],
        List[list[str, str]],
        List[list[bytes, bytes]],
        List[tuple[str, str]],
        List[tuple[bytes, bytes]],
        List[set[str, str]],
        List[set[bytes, bytes]],
    ]
]

CookieTypes = Optional[
    Union[
        "Cookies",
        CookieJar,
        Mapping[str, str],
        Mapping[bytes, bytes],
        List[list[str, str]],
        List[list[bytes, bytes]],
        List[tuple[str, str]],
        List[tuple[bytes, bytes]],
        List[set[str, str]],
        List[set[bytes, bytes]],
    ]
]

TimeoutTypes = Optional[Union[int, float]]
ProxyTypes = Union["URL", str, "Proxy"]

ByteOrStr = Union[bytes, str]
BufferTypes = Union[IO[bytes], "BytesIO", "BufferedReader"]
FileContent = Union[ByteOrStr, BinaryIO]
RequestFileValue = Union[
    FileContent,  # file (or file path, str and bytes)
    Tuple[ByteOrStr, FileContent],  # filename, file (or file path, str and bytes))
    Tuple[
        ByteOrStr, FileContent, ByteOrStr
    ],  # filename, file (or file path, str and bytes)), content type
]
RequestData = Mapping[str, Any]
RequestJson = Mapping[str, Any]
RequestFiles = Mapping[ByteOrStr, RequestFileValue]
ResponseHistory = List["Response"]
