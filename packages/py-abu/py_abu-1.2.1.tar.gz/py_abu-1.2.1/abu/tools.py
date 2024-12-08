# -*- coding: utf-8 -*-
# @Time    : 2024/8/8 10:37
# @Author  : Chris
# @Email   : 10512@qq.com
# @File    : tools.py
# @Software: PyCharm
import asyncio
import datetime
import os
import signal
import threading
import time
import traceback
from typing import Callable

from loguru import logger


def retry_with_method(max_attempts=9, retry_method=None, *closer_args, **closer_kwargs):
    """try to run the function for max_attempts times, if failed, run the retry_method"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    result = func(*args, **kwargs)
                    return result
                except BaseException:
                    logger.error(f"{func.__name__}运行过程错误正在重试第{attempts + 1}次!")
                    logger.error(traceback.format_exc())
                    retry_method and retry_method(
                        *args, *closer_args, **kwargs, **closer_kwargs)
                    attempts += 1
                    if attempts == max_attempts:
                        logger.error(f"{func.__name__}重试超过{attempts}次,放弃任务!")
                        break
                    time.sleep(3)
                    continue

        async def async_wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    result = await func(*args, **kwargs)
                    return result
                except BaseException:
                    logger.error(f"{func.__name__}运行过程错误正在重试第{attempts + 1}次!")
                    logger.error(traceback.format_exc())
                    retry_method and retry_method(
                        *args, *closer_args, **kwargs, **closer_kwargs)
                    attempts += 1
                    if attempts == max_attempts:
                        logger.error(f"{func.__name__}重试超过{attempts}次,放弃任务!")
                        break
                    await asyncio.sleep(3)
                    continue

        return wrapper if not asyncio.iscoroutinefunction(func) else async_wrapper

    return decorator


def wait_for_next_google_effect():
    t = datetime.datetime.now().second
    if t < 30:
        while datetime.datetime.now().second <= 30:
            time.sleep(1)
    else:
        while datetime.datetime.now().second >= 30:
            time.sleep(1)


async def wait_for_next_google_effect_async():
    t = datetime.datetime.now().second
    if t < 30:
        while datetime.datetime.now().second <= 30:
            await asyncio.sleep(1)
    else:
        while datetime.datetime.now().second >= 30:
            await asyncio.sleep(1)


def over(endingFunc: Callable = None) -> None:
    """结束程序"""
    if endingFunc:
        if asyncio.iscoroutinefunction(endingFunc):
            hasattr(
                asyncio, "WindowsSelectorEventLoopPolicy"
            ) and asyncio.set_event_loop_policy(
                asyncio.WindowsSelectorEventLoopPolicy()
            )
            asyncio.run(endingFunc())
        else:
            endingFunc()
    logger.warning("Process finished with exit code 15")
    os.kill(os.getpid(), signal.SIGTERM)


class SetInterval:
    def __init__(self, func, interval, *args, **kwargs):
        self.func = func
        self.func(*args, **kwargs)
        self.interval = interval
        self.args = args
        self.kwargs = kwargs
        self.timer = None
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.func(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self.timer = threading.Timer(self.interval, self._run)
            self.timer.start()
            self.is_running = True

    def stop(self):
        if self.timer:
            self.timer.cancel()
        self.is_running = False

    def cancel(self):
        self.stop()



