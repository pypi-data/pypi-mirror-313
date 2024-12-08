# -*- coding: utf-8 -*-
# @Time    : 2024/8/7 20:58
# @Author  : Chris
# @Email   : 10512@qq.com
# @File    : _2fa.py
# @Software: PyCharm

import base64
import datetime
import hmac
import time
from hashlib import sha1


def byte_secret(secret):
    missing_padding = len(secret) % 8

    if missing_padding != 0:
        secret += "=" * (8 - missing_padding)
    return base64.b32decode(secret, casefold=True)


def int_to_byte_string(i, padding=8):
    result = bytearray()
    while i != 0:
        result.append(i & 0xFF)
        i >>= 8
    return bytes(bytearray(reversed(result)).rjust(padding, b"\0"))


def get_2fa(secret):
    for_time = datetime.datetime.now()
    i = time.mktime(for_time.timetuple())
    inputInteger = int(i / 30)
    digest = sha1
    digits = 6
    if inputInteger < 0:
        raise ValueError("input must be positive integer")
    hasher = hmac.new(byte_secret(secret),
                      int_to_byte_string(inputInteger), digest)
    hmac_hash = bytearray(hasher.digest())
    offset = hmac_hash[-1] & 0xF
    code = (
            (hmac_hash[offset] & 0x7F) << 24
            | (hmac_hash[offset + 1] & 0xFF) << 16
            | (hmac_hash[offset + 2] & 0xFF) << 8
            | (hmac_hash[offset + 3] & 0xFF)
    )
    str_code = str(code % 10 ** digits)
    while len(str_code) < digits:
        str_code = "0" + str_code
    return str_code
