# _*_ coding : UTF-8 _*_
# 开发人员： XiaoqiangClub
# 微信公众号: XiaoqiangClub
# 开发时间：2024年06月13日
# 文件名称： sender.py
# 项目描述： 同步和异步发送消息的模块
import asyncio
from typing import Optional, Dict, Any
from xiaoqiangclub.api.message_sender.async_sender import AsyncMessageSender
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
from xiaoqiangclub.config.log_config import log


def _send_sync(func, *args, **kwargs) -> any:
    """
    通用的同步发送方法，处理发送过程中的异常。

    :param func: 发送函数。
    :param args: 发送函数的位置参数。
    :param kwargs: 发送函数的关键字参数。
    :return: bool，发送是否成功。
    """
    try:
        return asyncio.run(func(*args, **kwargs))
    except Exception as e:
        log.error(f"发送失败: {e}")
        return False


async def _send_async(func, *args, **kwargs) -> any:
    """
    通用的异步发送方法，处理发送过程中的异常。

    :param func: 发送函数。
    :param args: 发送函数的位置参数。
    :param kwargs: 发送函数的关键字参数。
    :return: bool，发送是否成功。
    """
    try:
        return await func(*args, **kwargs)
    except Exception as e:
        log.error(f"发送失败: {e}")
        return False


class MessageSender:
    @staticmethod
    def send_messages_sync(
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
    ):
        """
        同步方式发送消息到多个平台

        :param email_args: 邮件参数
        :param wechat_args: 微信参数
        :param dingtalk_args: 钉钉参数
        :param bark_args: Bark参数
        :param telegram_args: Telegram参数
        :param igot_args: IGot参数
        :param push_plus_args: push_plus参数
        :param an_push_args: an_push参数
        :param feishu_args: 飞书参数
        :param discord_args: Discord参数
        :param whatsapp_args: WhatsApp参数
        """
        return _send_sync(AsyncMessageSender.send_messages, email_args, wechat_args, dingtalk_args, bark_args,
                          telegram_args, igot_args, push_plus_args, an_push_args, feishu_args, discord_args,
                          whatsapp_args)

    @staticmethod
    def send_messages_with_config_sync(config_path: str, message: str, title: Optional[str] = None,
                                       url: Optional[str] = None) -> bool:
        """
        使用配置文件同步方式发送消息到多个平台

        :param config_path: 配置文件路径
        :param message: 消息内容
        :param title: 消息标题（可选）
        :param url: 消息链接（可选）
        """
        return _send_sync(AsyncMessageSender.send_messages_with_config, config_path, message, title, url)

    @staticmethod
    async def email_async(subject: str, body: str, to_email: str, from_email: str, smtp_server: str, smtp_port: int,
                          smtp_user: str, smtp_password: str) -> bool:
        """
        异步方式发送邮件

        :param subject: 邮件主题
        :param body: 邮件内容
        :param to_email: 收件人邮箱
        :param from_email: 发件人邮箱
        :param smtp_server: SMTP服务器地址
        :param smtp_port: SMTP服务器端口
        :param smtp_user: SMTP用户名
        :param smtp_password: SMTP密码
        """
        return await _send_async(EmailSender.send_email, subject, body, to_email, from_email, smtp_server, smtp_port,
                                 smtp_user, smtp_password)

    @staticmethod
    def email(subject: str, body: str, to_email: str, from_email: str, smtp_server: str, smtp_port: int, smtp_user: str,
              smtp_password: str) -> bool:
        """
        同步方式发送邮件

        :param subject: 邮件主题
        :param body: 邮件内容
        :param to_email: 收件人邮箱
        :param from_email: 发件人邮箱
        :param smtp_server: SMTP服务器地址
        :param smtp_port: SMTP服务器端口
        :param smtp_user: SMTP用户名
        :param smtp_password: SMTP密码
        """
        return _send_sync(EmailSender.send_email, subject, body, to_email, from_email, smtp_server, smtp_port,
                          smtp_user, smtp_password)

    @staticmethod
    async def wechat_async(wechat_corp_id: str, wechat_corp_secret: str, wechat_agent_id: int, message: str,
                           touser: str = "@all", toparty: str = "", totag: str = "") -> bool:
        """
        异步方式发送微信消息

        :param wechat_corp_id: 企业微信ID
        :param wechat_corp_secret: 企业微信密钥
        :param wechat_agent_id: 企业微信应用ID
        :param message: 消息内容
        :param touser: 接收消息的用户ID列表，多个用户用 '|' 分隔，默认为 '@all'
        :param toparty: 接收消息的部门ID列表，多个部门用 '|' 分隔
        :param totag: 接收消息的标签ID列表，多个标签用 '|' 分隔
        """
        return await _send_async(WeChatSender.send_wechat_message, wechat_corp_id, wechat_corp_secret, wechat_agent_id,
                                 message, touser, toparty, totag)

    @staticmethod
    def wechat(wechat_corp_id: str, wechat_corp_secret: str, wechat_agent_id: int, message: str, touser: str = "@all",
               toparty: str = "", totag: str = "") -> bool:
        """
        同步方式发送微信消息

        :param wechat_corp_id: 企业微信ID
        :param wechat_corp_secret: 企业微信密钥
        :param wechat_agent_id: 企业微信应用ID
        :param message: 消息内容
        :param touser: 接收消息的用户ID列表，多个用户用 '|' 分隔，默认为 '@all'
        :param toparty: 接收消息的部门ID列表，多个部门用 '|' 分隔
        :param totag: 接收消息的标签ID列表，多个标签用 '|' 分隔
        """
        return _send_sync(WeChatSender.send_wechat_message, wechat_corp_id, wechat_corp_secret, wechat_agent_id,
                          message, touser, toparty, totag)

    @staticmethod
    async def dingtalk_async(webhook_url: str, message: str, secret: str = None) -> bool:
        """
        异步方式发送钉钉消息

        :param webhook_url: 钉钉机器人Webhook地址
        :param message: 消息内容
        :param secret: 加签密钥（可选）
        """
        return await _send_async(DingTalkSender.send_dingtalk_message, webhook_url, message, secret)

    @staticmethod
    def dingtalk(webhook_url: str, message: str, secret: str = None) -> bool:
        """
        同步方式发送钉钉消息

        :param webhook_url: 钉钉机器人Webhook地址
        :param message: 消息内容
        :param secret: 加签密钥（可选）
        """
        return _send_sync(DingTalkSender.send_dingtalk_message, webhook_url, message, secret)

    @staticmethod
    async def bark_async(bark_url: str, message: str) -> bool:
        """
        异步方式发送Bark消息

        :param bark_url: Bark推送地址
        :param message: 消息内容
        """
        return await BarkSender.send_bark_message(bark_url, message)

    @staticmethod
    def bark(bark_url: str, message: str) -> bool:
        """
        同步方式发送Bark消息

        :param bark_url: Bark推送地址
        :param message: 消息内容
        """
        return _send_sync(BarkSender.send_bark_message, bark_url, message)

    @staticmethod
    async def telegram_async(bot_token: str, chat_id: str, message: str) -> bool:
        """
        异步方式发送Telegram消息

        :param bot_token: Telegram机器人Token
        :param chat_id: Telegram聊天ID
        :param message: 消息内容
        """
        return _send_async(TelegramSender.send_telegram_message, bot_token, chat_id, message)

    @staticmethod
    def telegram(bot_token: str, chat_id: str, message: str) -> bool:
        """
        同步方式发送Telegram消息

        :param bot_token: Telegram机器人Token
        :param chat_id: Telegram聊天ID
        :param message: 消息内容
        """
        return _send_sync(TelegramSender.send_telegram_message, bot_token, chat_id, message)

    @staticmethod
    async def igot_async(igot_key: str, message: str) -> bool:
        """
        异步方式发送IGot消息

        :param igot_key: IGot密钥
        :param message: 消息内容
        """
        return await _send_async(IGotSender.send_igot_message, igot_key, message)

    @staticmethod
    def igot(igot_key: str, message: str) -> bool:
        """
        同步方式发送IGot消息

        :param igot_key: IGot密钥
        :param message: 消息内容
        """
        return _send_sync(IGotSender.send_igot_message, igot_key, message)

    @staticmethod
    async def push_plus_async(token: str, message: str) -> bool:
        """
        异步方式发送push_plus消息

        :param token: push_plus Token
        :param message: 消息内容
        """
        return _send_async(PushPlusSender.send_push_plus_message, token, message)

    @staticmethod
    def push_plus(token: str, message: str) -> bool:
        """
        同步方式发送push_plus消息

        :param token: push_plus Token
        :param message: 消息内容
        """
        return _send_sync(PushPlusSender.send_push_plus_message, token, message)

    @staticmethod
    async def an_push_async(token: str, title: str, message: str, url: str = None) -> bool:
        """
        异步方式发送an_push消息

        :param token: an_push Token
        :param title: 消息标题
        :param message: 消息内容
        :param url: 消息链接（可选）
        """
        return _send_async(AnPushSender.send_an_push_message, token, title, message, url)

    @staticmethod
    def an_push(token: str, title: str, message: str, url: str = None) -> bool:
        """
        同步方式发送an_push消息

        :param token: an_push Token
        :param title: 消息标题
        :param message: 消息内容
        :param url: 消息链接（可选）
        """
        return _send_sync(AnPushSender.send_an_push_message, token, title, message, url)

    @staticmethod
    async def feishu_async(webhook_url: str, message: str) -> bool:
        """
        异步方式发送飞书消息

        :param webhook_url: 飞书机器人Webhook地址
        :param message: 消息内容
        """
        return _send_async(FeishuSender.send_feishu_message, webhook_url, message)

    @staticmethod
    def feishu(webhook_url: str, message: str) -> bool:
        """
        同步方式发送飞书消息

        :param webhook_url: 飞书机器人Webhook地址
        :param message: 消息内容
        """
        return _send_sync(FeishuSender.send_feishu_message, webhook_url, message)

    @staticmethod
    async def discord_async(webhook_url: str, message: str) -> bool:
        """
        异步方式发送Discord消息

        :param webhook_url: Discord Webhook地址
        :param message: 消息内容
        """
        return _send_async(DiscordSender.send_discord_message, webhook_url, message)

    @staticmethod
    def discord(webhook_url: str, message: str) -> bool:
        """
        同步方式发送Discord消息

        :param webhook_url: Discord Webhook地址
        :param message: 消息内容
        """
        return _send_sync(DiscordSender.send_discord_message, webhook_url, message)

    @staticmethod
    async def whatsapp_async(api_url: str, phone_number: str, message: str, api_token: str) -> bool:
        """
        异步方式发送WhatsApp消息

        :param api_url: WhatsApp API URL
        :param phone_number: 接收消息的电话号码
        :param message: 消息内容
        :param api_token: API Token
        """
        return await WhatsAppSender.send_whatsapp_message(api_url, phone_number, message, api_token)

    @staticmethod
    def whatsapp(api_url: str, phone_number: str, message: str, api_token: str) -> bool:
        """
        同步方式发送WhatsApp消息

        :param api_url: WhatsApp API URL
        :param phone_number: 接收消息的电话号码
        :param message: 消息内容
        :param api_token: API Token
        """
        return _send_sync(WhatsAppSender.send_whatsapp_message, api_url, phone_number, message, api_token)

    @staticmethod
    async def send_messages_async(
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
    ):
        """
        异步方式发送消息到多个平台

        :param email_args: 邮件参数
        :param wechat_args: 微信参数
        :param dingtalk_args: 钉钉参数
        :param bark_args: Bark参数
        :param telegram_args: Telegram参数
        :param igot_args: IGot参数
        :param push_plus_args: push_plus参数
        :param an_push_args: an_push参数
        :param feishu_args: 飞书参数
        :param discord_args: Discord参数
        :param whatsapp_args: WhatsApp参数
        """
        return _send_async(AsyncMessageSender.send_messages, email_args, wechat_args, dingtalk_args, bark_args,
                           telegram_args,
                           igot_args, push_plus_args, an_push_args, feishu_args, discord_args, whatsapp_args)

    @staticmethod
    async def send_messages_with_config_async(config_path: str, message: str, title: Optional[str] = None,
                                              url: Optional[str] = None):
        """
        使用配置文件异步方式发送消息到多个平台

        :param config_path: 配置文件路径
        :param message: 消息内容
        :param title: 消息标题（可选）
        :param url: 消息链接（可选）
        """
        return _send_async(AsyncMessageSender.send_messages_with_config, config_path, message, title, url)
