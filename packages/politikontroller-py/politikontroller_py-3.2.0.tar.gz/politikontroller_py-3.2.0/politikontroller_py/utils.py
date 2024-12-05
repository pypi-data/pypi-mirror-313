from __future__ import annotations

import base64
from datetime import datetime, time as dt_time
from json import JSONDecoder, JSONEncoder
from logging import getLogger
import random
import re
import string
import time

from Crypto.Cipher import AES

from .constants import (
    CRYPTO_K1,
    CRYPTO_K2,
)

_LOGGER = getLogger(__name__)
JUNK_CHARS = "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x10\x0f"


def get_random_string(length: int, letters: str | None = None) -> str:
    if letters is None:
        letters = string.ascii_uppercase + string.digits
    return "".join(random.choice(letters) for _ in range(length))


def generate_device_id():
    return get_random_string(16, letters=string.digits + "abcdef")


def get_unix_timestamp():
    return int(time.time()) + 10


def hash_credentials(credentials: dict):
    creds = bytes(JSONEncoder().encode(credentials), "utf-8")
    return base64.b64encode(creds).decode()


def unhash_credentials(credentials: str):
    creds = base64.b64decode(credentials).decode()
    return JSONDecoder().decode(creds)


def aes_encrypt(input_str: str):
    """Encrypts a string using AES encryption with given key and initialization vector.
    Returns base64-encoded result.
    """
    key = base64.b64decode(CRYPTO_K2)
    iv = base64.b64decode(CRYPTO_K1)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    length = 16 - (len(input_str) % 16)
    input_b = bytes(input_str, "utf-8") + bytes([length]) * length
    return base64.b64encode(cipher.encrypt(input_b)).decode()


def aes_decrypt(enc_base64: str):
    """Decrypts AES encrypted data using a given key and initialization vector."""
    enc_data = base64.b64decode(enc_base64)
    key = base64.b64decode(CRYPTO_K2)
    iv = base64.b64decode(CRYPTO_K1)
    decipher = AES.new(key, AES.MODE_CBC, iv)
    return decipher.decrypt(enc_data).decode().strip(JUNK_CHARS).strip()


def map_response_data(
    data: str, map_keys: list[str | None], multiple=False
) -> list[dict[str, str]] | dict[str, str]:
    """Convert a cvs-like string into dictionaries."""

    def row_to_dict(row) -> dict[str, str]:
        r = dict(zip(map_keys, row.split("|")))
        return {k: r[k] for k in r if isinstance(k, str)}

    if multiple:
        return list(map(row_to_dict, list(data.split("#"))))

    return row_to_dict(data)


def parse_datetime_like(v: str) -> int | None:
    if len(v) == 0 or (v.isnumeric() and int(v) == 0):
        return None
    return int(parse_time_format(v))


def parse_time_format(text: str) -> int | str:
    today = datetime.now().astimezone()
    try:
        # Match "%d.%m - %H:%M" this way due to failure on leap days using strptime.
        if m := re.match(r"(\d{2})\.(\d{2}) - (\d{2}):(\d{2})", text):
            return int(
                datetime.fromisoformat(f"{today.year}-{m[2]}-{m[1]}T{m[3]}:{m[4]}:00")
                .astimezone()
                .timestamp()
            )
    except ValueError:
        pass

    try:
        return int(
            datetime.combine(
                today,
                dt_time.fromisoformat(text),
            )
            .astimezone()
            .timestamp()
        )
    except ValueError:
        pass

    try:
        text = re.sub(r"(\d{2}:\d{2})(?: \(\d+ ganger\))?", "\\1", text)
        return int(
            datetime.strptime(text, "%H:%M")
            .astimezone()
            .replace(
                year=today.year,
                month=today.month,
                day=today.day,
            )
            .timestamp()
        )
    except ValueError:
        pass
    return text
