# _*_ coding : UTF-8 _*_
# 开发人员： XiaoqiangClub
# 微信公众号: XiaoqiangClub
# 开发时间：2024年06月13日
# 文件名称： push_plus_sender.py
# 项目描述： 发送push_plus消息的模块

import httpx
from typing import Dict
from xiaoqiangclub.config.log_config import log


class PushPlusSender:
    @staticmethod
    async def send_push_plus_message(token: str, message: str) -> bool:
        """
        发送push_plus消息。

        :param token: push_plus Token，字符串类型。
        :param message: 消息内容，字符串类型。
        获取push_plus参数：https://www.push_plus.plus/
        :return: 消息发送成功返回 True，否则返回 False。
        """
        async with httpx.AsyncClient() as client:
            try:
                send_url = "http://www.push_plus.plus/send"
                data = {
                    "token": token,
                    "content": message
                }
                response = await client.post(send_url, json=data)
                if response.status_code == 200:
                    log.info("push_plus消息发送成功")
                    return True
                else:
                    log.error(f"push_plus消息发送失败: {response.status_code}")
                    return False
            except Exception as e:
                log.error(f"push_plus消息发送失败: {e}")
                return False

    @staticmethod
    async def send_push_plus_message_with_config(config: Dict[str, Dict[str, str]], message: str) -> bool:
        """
        使用配置文件发送push_plus消息。

        :param config: 配置字典，字典类型，包含 push_plus 的配置信息。
        :param message: 消息内容，字符串类型。
        :return: 消息发送成功返回 True，否则返回 False。
        """
        push_plus_config = config['push_plus']
        return await PushPlusSender.send_push_plus_message(
            token=push_plus_config['token'],
            message=message
        )
