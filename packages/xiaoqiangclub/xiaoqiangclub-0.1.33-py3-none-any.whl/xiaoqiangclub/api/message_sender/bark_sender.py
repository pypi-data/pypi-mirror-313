# _*_ coding : UTF-8 _*_
# 开发人员： XiaoqiangClub
# 微信公众号: XiaoqiangClub
# 开发时间：2024年06月13日
# 文件名称： bark_sender.py
# 项目描述： 发送Bark消息的模块

from typing import Dict, Optional
from xiaoqiangclub.config.log_config import log
import httpx


class BarkSender:
    @staticmethod
    async def send_bark_message(bark_url: str, message: str) -> bool:
        """
        发送Bark消息。

        :param bark_url: Bark推送地址，字符串类型。
        :param message: 消息内容，字符串类型。
        获取Bark参数：https://github.com/Finb/Bark
        :return: 消息发送成功返回 True，否则返回 False。
        """
        async with httpx.AsyncClient() as client:
            try:
                send_url = f"{bark_url}/{message}"
                response = await client.get(send_url)
                if response.status_code == 200:
                    log.info("Bark消息发送成功")
                    return True
                else:
                    log.error(f"Bark消息发送失败: {response.status_code}, 响应: {response.text}")
                    return False
            except Exception as e:
                log.error(f"Bark消息发送失败: {e}")
                return False

    @staticmethod
    async def send_bark_message_with_config(config: Dict[str, str], message: str) -> bool:
        """
        使用配置文件发送Bark消息。

        :param config: 配置字典，字典类型，包含 bark 的配置信息。
        :param message: 消息内容，字符串类型。
        :return: 消息发送成功返回 True，否则返回 False。
        """
        bark_config = config['bark']
        return await BarkSender.send_bark_message(
            bark_url=bark_config['bark_url'],
            message=message
        )
