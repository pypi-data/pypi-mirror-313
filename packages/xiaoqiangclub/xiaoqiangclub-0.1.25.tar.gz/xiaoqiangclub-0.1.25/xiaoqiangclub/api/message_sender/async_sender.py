# _*_ coding : UTF-8 _*_
# 开发人员： XiaoqiangClub
# 微信公众号: XiaoqiangClub
# 开发时间：2024年06月13日
# 文件名称： async_sender.py
# 项目描述： 异步发送消息的模块

import asyncio
from typing import Optional, Dict, Any
from xiaoqiangclub.api.message_sender.email_sender import EmailSender
from xiaoqiangclub.api.message_sender.wechat_sender import WeChatSender
from xiaoqiangclub.api.message_sender.dingtalk_sender import DingTalkSender
from xiaoqiangclub.api.message_sender.bark_sender import BarkSender
from xiaoqiangclub.api.message_sender.telegram_sender import TelegramSender
from xiaoqiangclub.api.message_sender.igot_sender import IGotSender
from xiaoqiangclub.api.message_sender.push_plus_sender import PushPlusSender
from xiaoqiangclub.api.message_sender.an_push_sender import AnPushSender
from xiaoqiangclub.api.message_sender.feishu_sender import FeishuSender
from xiaoqiangclub.api.message_sender.discord_sender import DiscordSender
from xiaoqiangclub.api.message_sender.whatsapp_sender import WhatsAppSender
from xiaoqiangclub.api.message_sender.config_loader import ConfigLoader


class AsyncMessageSender:
    @staticmethod
    async def send_messages(
            email_args: Optional[Dict[str, Any]] = None,
            wechat_args: Optional[Dict[str, Any]] = None,
            dingtalk_args: Optional[Dict[str, Any]] = None,
            bark_args: Optional[Dict[str, Any]] = None,
            telegram_args: Optional[Dict[str, Any]] = None,
            igot_args: Optional[Dict[str, Any]] = None,
            push_plus_args: Optional[Dict[str, Any]] = None,
            an_push_args: Optional[Dict[str, Any]] = None,
            feishu_args: Optional[Dict[str, Any]] = None,
            discord_args: Optional[Dict[str, Any]] = None,
            whatsapp_args: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        异步发送消息

        :param email_args: 邮件发送参数
        :param wechat_args: 微信发送参数
        :param dingtalk_args: 钉钉发送参数
        :param bark_args: Bark发送参数
        :param telegram_args: Telegram发送参数
        :param igot_args: IGot发送参数
        :param push_plus_args: push_plus发送参数
        :param an_push_args: AnPush发送参数
        :param feishu_args: 飞书发送参数
        :param discord_args: Discord发送参数
        :param whatsapp_args: WhatsApp发送参数
        """
        tasks = []  # 存储所有发送任务

        if email_args:
            tasks.append(EmailSender.send_email(**email_args))
        if wechat_args:
            tasks.append(WeChatSender.send_wechat_message(**wechat_args))
        if dingtalk_args:
            tasks.append(DingTalkSender.send_dingtalk_message(**dingtalk_args))
        if bark_args:
            tasks.append(BarkSender.send_bark_message(**bark_args))
        if telegram_args:
            tasks.append(TelegramSender.send_telegram_message(**telegram_args))
        if igot_args:
            tasks.append(IGotSender.send_igot_message(**igot_args))
        if push_plus_args:
            tasks.append(PushPlusSender.send_push_plus_message(**push_plus_args))
        if an_push_args:
            tasks.append(AnPushSender.send_an_push_message(**an_push_args))
        if feishu_args:
            tasks.append(FeishuSender.send_feishu_message(**feishu_args))
        if discord_args:
            tasks.append(DiscordSender.send_discord_message(**discord_args))
        if whatsapp_args:
            tasks.append(WhatsAppSender.send_whatsapp_message(**whatsapp_args))

        await asyncio.gather(*tasks)  # 等待所有任务完成

    @staticmethod
    async def send_messages_with_config(config_path: str, message: str, title: Optional[str] = None,
                                        url: Optional[str] = None) -> None:
        """
        使用配置文件发送消息

        :param config_path: 配置文件路径
        :param message: 消息内容
        :param title: 消息标题（可选）
        :param url: 消息链接（可选）
        """
        config = ConfigLoader.load_config(config_path)  # 加载配置文件
        tasks = []  # 存储所有发送任务

        # 根据配置发送消息
        if 'email' in config:
            email_config = config['email']
            tasks.append(EmailSender.send_email_with_config(email_config, title or "Message", message))
        if 'wechat' in config:
            wechat_config = config['wechat']
            tasks.append(WeChatSender.send_wechat_message_with_config(wechat_config, message))
        if 'dingtalk' in config:
            dingtalk_config = config['dingtalk']
            tasks.append(DingTalkSender.send_dingtalk_message_with_config(dingtalk_config, message))
        if 'bark' in config:
            bark_config = config['bark']
            tasks.append(BarkSender.send_bark_message_with_config(bark_config, message))
        if 'telegram' in config:
            telegram_config = config['telegram']
            tasks.append(TelegramSender.send_telegram_message_with_config(telegram_config, message))
        if 'igot' in config:
            igot_config = config['igot']
            tasks.append(IGotSender.send_igot_message_with_config(igot_config, message))
        if 'push_plus' in config:
            push_plus_config = config['push_plus']
            tasks.append(PushPlusSender.send_push_plus_message_with_config(push_plus_config, message))
        if 'anpush' in config:
            anpush_config = config['anpush']
            tasks.append(AnPushSender.send_an_push_message_with_config(anpush_config, title or "Message", message, url))
        if 'feishu' in config:
            feishu_config = config['feishu']
            tasks.append(FeishuSender.send_feishu_message_with_config(feishu_config, message))
        if 'discord' in config:
            discord_config = config['discord']
            tasks.append(DiscordSender.send_discord_message_with_config(discord_config, message))
        if 'whatsapp' in config:
            whatsapp_config = config['whatsapp']
            tasks.append(WhatsAppSender.send_whatsapp_message_with_config(whatsapp_config, message))

        await asyncio.gather(*tasks)  # 等待所有任务完成
