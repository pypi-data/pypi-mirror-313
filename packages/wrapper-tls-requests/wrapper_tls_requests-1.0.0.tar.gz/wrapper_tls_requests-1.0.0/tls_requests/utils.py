from __future__ import annotations

import base64
import importlib
import logging
import typing
from typing import Any, Union

FORMAT = "%(levelname)s:%(asctime)s:%(_name)s:%(funcName)s:%(lineno)d >>> %(message)s"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def import_module(name: Union[str, list[str]]):
    modules = name if isinstance(name, list) else [name]
    for module in modules:
        if isinstance(module, str):
            try:
                module = importlib.import_module(module)
                return module
            except ImportError:
                pass


chardet = import_module(["chardet", "charset_normalizer"])
orjson = import_module(["orjson"])
if orjson:
    jsonlib = orjson
else:
    import json

    jsonlib = json


def get_logger(
    name: str = "TLSRequests", level: int | str = logging.INFO
) -> logging.Logger:
    logging.basicConfig(format=FORMAT, datefmt=DATE_FORMAT, level=level)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger


def primitive_value_to_str(value) -> str:
    """
    Coerce a primitive data type into a string value.

    Note that we prefer JSON-style 'true'/'false' for boolean values here.
    """
    if value is True:
        return "true"
    elif value is False:
        return "false"
    elif value is None:
        return ""
    return str(value)


def to_bytes(value: Any, encoding: str = "utf-8", *, lower: bool = False) -> bytes:
    if isinstance(value, (bytes, bytearray)):
        return value
    return to_str(value, encoding).encode(encoding)


def to_str(
    value: Any,
    encoding: str = "utf-8",
    *,
    lower: bool = False,
) -> str:
    if value is None:
        return ""

    value = value.decode(encoding) if isinstance(value, (bytes, bytearray)) else value
    if isinstance(value, (dict, list, tuple, set)):
        value = json_dumps(
            value if isinstance(value, dict) else list[value],
            **dict(
                ensure_ascii=True if str(encoding).lower() == "ascii" else False,
                default=str,
            ),
        )

    if isinstance(value, bool):
        lower = True

    if lower:
        return str(value).lower()

    return str(value)


def to_base64(value: Union[dict, str, bytes], encoding: str = "utf-8") -> typing.AnyStr:
    return base64.b64encode(to_bytes(value, encoding)).decode(encoding)


def to_json(value: Union[str, bytes], encoding: str = "utf-8", **kwargs) -> dict:
    if isinstance(value, dict):
        return value
    if isinstance(value, bytes):
        value = value.decode(encoding, errors="ignore")
    try:
        json_data = jsonlib.loads(value, **kwargs)
        return json_data
    except jsonlib.JSONDecodeError:
        raise jsonlib.JSONDecodeError


def json_dumps(value, **kwargs) -> str:
    try:
        if orjson:
            kwargs = {"default": kwargs.pop("default", None)}

        json_data = jsonlib.dumps(value, **kwargs)
        if isinstance(json_data, bytes):
            json_data = json_data.decode("utf-8")
        return json_data
    except jsonlib.JSONDecodeError:
        raise jsonlib.JSONDecodeError
