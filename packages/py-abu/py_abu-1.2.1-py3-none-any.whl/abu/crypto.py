# -*- coding: utf-8 -*-
# @Time    : 2024/8/14 16:01
# @Author  : Chris
# @Email   : 10512@qq.com
# @File    : crypto.py
# @Software: PyCharm
import hmac
from hashlib import md5, sha1, sha256, sha512


def crypto_md5(originString: str) -> str:
    return md5(originString.encode("utf-8")).hexdigest()


def crypto_sha1(originString: str) -> str:
    return sha1(originString.encode("utf-8")).hexdigest()


def crypto_sha256(originString: str) -> str:
    return sha256(originString.encode("utf-8")).hexdigest()


def crypto_sha512(originString: str) -> str:
    return sha512(originString.encode("utf-8")).hexdigest()


def crypto_HMAC_MD5(key: str, originString: str) -> str:
    return hmac.new(key.encode("utf-8"), originString.encode("utf-8"), md5).hexdigest()
