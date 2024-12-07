# _*_ coding : UTF-8 _*_
# 开发人员： XiaoqiangClub
# 微信公众号: XiaoqiangClub
# 开发时间：2024年06月13日
# 文件名称： discord_sender.py
# 项目描述： 发送Discord消息的模块

import httpx
from typing import Dict
from xiaoqiangclub.config.log_config import log


class DiscordSender:
    @staticmethod
    async def send_discord_message(webhook_url: str, message: str) -> bool:
        """
        发送Discord消息。

        :param webhook_url: Discord Webhook地址，字符串类型。
        :param message: 消息内容，字符串类型。
        获取Discord Webhook参数：https://discord.com/developers/docs/resources/webhook
        :return: 消息发送成功返回 True，否则返回 False。
        """
        async with httpx.AsyncClient() as client:
            try:
                headers = {
                    "Content-Type": "application/json"
                }
                data = {
                    "content": message
                }
                response = await client.post(webhook_url, headers=headers, json=data)
                if response.status_code == 204:
                    log.info("Discord消息发送成功")
                    return True
                else:
                    log.error(f"Discord消息发送失败: {response.status_code}")
                    return False
            except Exception as e:
                log.error(f"Discord消息发送失败: {e}")
                return False

    @staticmethod
    async def send_discord_message_with_config(config: Dict[str, str], message: str) -> bool:
        """
        使用配置文件发送Discord消息。

        :param config: 配置字典，字典类型，包含 discord 的配置信息。
        :param message: 消息内容，字符串类型。
        :return: 消息发送成功返回 True，否则返回 False。
        """
        discord_config = config['discord']
        return await DiscordSender.send_discord_message(
            webhook_url=discord_config['webhook_url'],
            message=message
        )
