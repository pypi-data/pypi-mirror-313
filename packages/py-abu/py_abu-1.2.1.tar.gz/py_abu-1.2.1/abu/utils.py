# -*- coding: utf-8 -*-
# @Time    : 2024/8/7 18:42
# @Author  : Chris
# @Email   : 10512@qq.com
# @File    : utils.py
# @Software: PyCharm
import asyncio
import json
import random
import string
import threading
from types import SimpleNamespace

import pyperclip
from aiohttp import CookieJar


def json_to_object(_json: dict | str) -> SimpleNamespace:
    return json.loads(_json if type(_json) is str else json.dumps(_json),
                      object_hook=lambda d: SimpleNamespace(**d))


def text_mid(target_str: str, front_str: str, back_str: str, start_position: int = 0) -> str:
    """老一辈的易语言用户的心中, 一定有一个文本取中间...哈哈哈"""
    try:
        front_pos = target_str.index(front_str, start_position) + len(front_str)
        back_pos = target_str.index(back_str, front_pos)
        return target_str[front_pos: back_pos]
    except ValueError:
        return ""


def text_random_str(count: int = 1) -> str:
    result = random.choice(string.ascii_letters)
    letters = string.ascii_letters + string.digits
    for i in range(count - 1):
        result += random.choice(letters)
    return result


def set_timeout(func, delay, *args, **kwargs):
    timer = threading.Timer(delay, func, args, kwargs)
    timer.start()
    return timer


def set_clipboard_text(text: str) -> None:
    pyperclip.copy(text)


def get_clipboard_text() -> str:
    return pyperclip.paste()


def flatten_list(lst):
    """展开数组"""
    result = []
    for item in lst:
        if isinstance(item, (list, tuple)):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result


def set_cookie_to_chrome(cookiePath: str) -> str:
    """
    get cookie from aiohttp to Chrome.
    :param cookiePath: 'F:\\AutoBackups\\Code\\PythonProjects\\temp\\90491@qq.com.cookie'
    :return: str
    """

    ret = (
        "function setCookie(cookieName,value,expiresTime,path){expiresTime=expiresTime||"
        '"Thu, 01-Jan-2030 00:00:01 GMT";path=path||"/";document.cookie=cookieName+"="+'
        '(value.includes("%")?value:encodeURIComponent(value))+"; expires="+expiresTime+"; path="+path;}'
    )
    jar = CookieJar(loop=asyncio.new_event_loop())
    jar.load(cookiePath)
    for v in dict(getattr(jar, "_cookies")).values():
        for x in getattr(v, "values")():
            ret += f'setCookie(`{x.key}`,`{x.value}`);'
    set_clipboard_text(ret)
    return ret
