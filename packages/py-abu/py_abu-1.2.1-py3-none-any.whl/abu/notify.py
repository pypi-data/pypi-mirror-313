# -*- coding: utf-8 -*-
# @Time    : 2024/8/8 14:52
# @Author  : Chris
# @Email   : 10512@qq.com
# @File    : notify.py
# @Software: PyCharm
import time

import requests
from loguru import logger

from abu import retry_with_method


@retry_with_method(3)
def send_msg_to_telegram(bot_token, chat_id, content, proxy: str = '') -> bool:
    """
    通过telegram机器人发消息给指定用户或群组
    :param bot_token:   机器人token
    :param chat_id:     用户或群组id
    :param content:     发送的内容
    :param proxy:       telegram在国内需要使用国外代理
    :return:            发送成功返回True
    """
    for _ in range(3):
        try:
            data = {
                "chat_id": chat_id,
                "text": content,
                "parse_mode": "MarkdownV2"
            }
            if proxy:
                ret = requests.post(f"https://api.telegram.org/{bot_token}/sendMessage", data=data, verify=False,
                                    proxies={"https": proxy if proxy.startswith("http") else "http://" + proxy}).json()
            else:
                ret = requests.post(f"https://api.telegram.org/{bot_token}/sendMessage", data=data).json()

            if ret.get("ok"):
                logger.success("发送Telegram消息成功！")
                return True
            else:
                logger.error(f"推送消息失败.. {content}")
                return False
        except BaseException as e:
            logger.error(e.__repr__())

    return False


@retry_with_method(3)
def send_msg_to_bark(api, title: str = "Message", body: str = ""):
    """
    通过bark推送消息
    :param api:     bark的api
    :param title:   标题
    :param body:    内容
    """
    data = {"body": body, "title": title}
    for _ in range(3):
        try:
            ret = requests.post(
                f"{api}/?icon=https://i.bmp.ovh/imgs/2021/11/7995dd6ff8ae2e74.png",
                headers={
                    "Content-Type": "application/json; charset=utf-8",
                },
                json=data,
            ).json()

            if ret.get("code") == 200:
                logger.success(f"推送消息成功")
                break
            else:
                logger.error(f"推送消息失败..将在10秒后重新尝试...")
                time.sleep(9)
                continue
        except BaseException:
            time.sleep(9)


@retry_with_method(3)
def send_msg_to_wechat(bot_url, msg: str = "", to_abu: bool = False, wxid: str = ""):
    if to_abu:
        wxid = "mojun735396"
    for _ in range(3):
        ret = requests.post(bot_url, json={"type": "Q0001", "data": {"wxid": wxid, "msg": msg}}).json()
        if ret.get("code") == 200:
            break
        else:
            logger.error(ret)
            time.sleep(3)
