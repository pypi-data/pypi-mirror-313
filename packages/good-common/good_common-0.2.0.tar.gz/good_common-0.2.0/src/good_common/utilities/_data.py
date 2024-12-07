import base64
import typing

import farmhash
import datetime
from ._dates import parse_timestamp
from ._strings import encode_base32
from loguru import logger

T = typing.TypeVar("T", bound=type)


# def type_converter(from_: type, to_: T) -> typing.Callable[[str], typing.Optional[T]]:
#     def _converter(value) -> typing.Optional[T]:
#         if not value:
#             return value
#         try:
#             match from_, to_:
#                 case (str, datetime.datetime):
#                     return parse_timestamp(value)
#                 case (str, datetime.date):
#                     dt = parse_timestamp(value)
#                     return dt.date() if dt else None
#                 case (str, int):
#                     return int(value)
#                 case (str, float):
#                     return float(value)
#                 case (str, bool):
#                     return value.lower() == "true"
#                 case (int, str):
#                     return str(value)
#                 case (float, str):
#                     return str(value)
#                 case (bool, str):
#                     return str(value)

#         except Exception as e:
#             logger.debug(e)
#             return None
#         return value

#     return _converter


def is_int(string) -> bool:
    try:
        int(string)
        return True
    except ValueError:
        return False


def to_int(v) -> typing.Optional[int]:
    try:
        return int(v)
    except ValueError:
        return None


def signed_64_to_unsigned_128(num):
    # Python automatically handles integer promotion to larger bit widths.
    # For a negative number, add 2^64 to shift its representation to the upper 64 bits of the 128-bit space.
    return num + (1 << 64) if num < 0 else num


def int_to_base62(num):
    # Characters to be used in base-62 encoding
    characters = (
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"  # # noqa: E501
    )

    if num == 0:
        return characters[0]

    num = signed_64_to_unsigned_128(num)

    base62 = []
    while num:
        num, remainder = divmod(num, 62)
        base62.append(characters[remainder])

    # The final string is built in reverse
    return "".join(reversed(base62))


def to_float(v) -> typing.Optional[float]:
    try:
        return float(v)
    except ValueError:
        return None


def to_numeric(v) -> typing.Optional[typing.Union[int, float]]:
    try:
        return int(v)
    except ValueError:
        try:
            return float(v)
        except ValueError:
            return None


def farmhash_string(s: str) -> str:
    return encode_base32(farmhash.hash64(s))


def farmhash_bytes(s: str) -> bytes:
    return farmhash.hash64(s).to_bytes(8, "big")


def farmhash_hex(s: str) -> str:
    return farmhash_bytes(s).hex()


def b64_decode(string: typing.Any) -> str:
    """Decode a base64 string"""

    if not isinstance(string, str):
        string = str(string)

    # check if string is base64
    try:
        if base64.b64encode(base64.b64decode(string)).decode("utf-8") == string:
            return base64.b64decode(string).decode("utf-8")
    except Exception:
        pass
    return string


def b64_encode(string: typing.Any) -> str:
    """Encode a string to base64"""

    if not isinstance(string, str):
        string = str(string)

    return base64.b64encode(string.encode("utf-8")).decode("utf-8")
