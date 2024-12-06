# _*_ coding : UTF-8 _*_
# 开发人员： XiaoqiangClub
# 微信公众号: XiaoqiangClub
# 开发时间：2024年06月13日
# 文件名称： telegram_sender.py
# 项目描述： 发送Telegram消息的模块

import httpx
from typing import Dict
from xiaoqiangclub.config.log_config import log


class TelegramSender:
    @staticmethod
    async def send_telegram_message(bot_token: str, chat_id: str, message: str) -> bool:
        """
        发送Telegram消息。

        :param bot_token: Telegram机器人Token，字符串类型。
        :param chat_id: Telegram聊天ID，字符串类型。
        :param message: 消息内容，字符串类型。
        获取Telegram参数：https://core.telegram.org/bots/api
        :return: 消息发送成功返回 True，否则返回 False。
        """
        async with httpx.AsyncClient() as client:
            try:
                send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                data = {
                    "chat_id": chat_id,
                    "text": message
                }
                response = await client.post(send_url, json=data)
                if response.status_code == 200:
                    log.info("Telegram消息发送成功")
                    return True
                else:
                    log.error(f"Telegram消息发送失败: {response.status_code}")
                    return False
            except Exception as e:
                log.error(f"Telegram消息发送失败: {e}")
                return False

    @staticmethod
    async def send_telegram_message_with_config(config: Dict[str, Dict[str, str]], message: str) -> bool:
        """
        使用配置文件发送Telegram消息。

        :param config: 配置字典，字典类型，包含 telegram 的配置信息。
        :param message: 消息内容，字符串类型。
        :return: 消息发送成功返回 True，否则返回 False。
        """
        telegram_config = config['telegram']
        return await TelegramSender.send_telegram_message(
            bot_token=telegram_config['bot_token'],
            chat_id=telegram_config['chat_id'],
            message=message
        )
