# _*_ coding : UTF-8 _*_
# 开发人员： XiaoqiangClub
# 微信公众号: XiaoqiangClub
# 开发时间：2024 年 06 月 13 日
# 文件名称： an_push_sender.py
# 项目描述：发送 AnPush 消息的模块

from typing import Dict, Optional
from xiaoqiangclub.config.log_config import log
import httpx


class AnPushSender:
    @staticmethod
    async def send_an_push_message(token: str, title: str, message: str, url: Optional[str] = None) -> bool:
        """
        发送 AnPush 消息。

        :param token: AnPush Token，字符串类型。
        :param title: 消息标题，字符串类型。
        :param message: 消息内容，字符串类型。
        :param url: 消息链接（可选），字符串类型或 None。
        获取 AnPush 参数：https://www.anpush.com/
        :return: 消息发送成功返回 True，否则返回 False。
        """
        async with httpx.AsyncClient() as client:
            try:
                send_url = "https://api.anpush.com/send"
                data = {
                    "token": token,
                    "title": title,
                    "content": message,
                    "url": url
                }
                response = await client.post(send_url, json=data)
                if response.status_code == 200:
                    log.info(f"AnPush 消息发送成功: {response.json()}")
                    return True
                else:
                    log.error(f"AnPush 消息发送失败，状态码: {response.status_code}, 响应: {response.text}")
                    return False
            except Exception as e:
                log.error(f"AnPush 消息发送失败: {e}")
                return False

    @staticmethod
    async def send_an_push_message_with_config(config: Dict[str, Dict[str, str]], title: str, message: str,
                                               url: Optional[str] = None) -> bool:
        """
        使用配置文件发送 AnPush 消息。

        :param config: 配置字典，字典类型，包含 an_push 的配置信息。
        :param title: 消息标题，字符串类型。
        :param message: 消息内容，字符串类型。
        :param url: 消息链接（可选），字符串类型或 None。
        :return: 消息发送成功返回 True，否则返回 False。
        """
        an_push_config = config['an_push']
        return await AnPushSender.send_an_push_message(
            token=an_push_config['token'],
            title=title,
            message=message,
            url=url
        )
