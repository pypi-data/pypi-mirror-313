# _*_ coding : UTF-8 _*_
# 开发人员： XiaoqiangClub
# 微信公众号: XiaoqiangClub
# 开发时间：2024年06月13日
# 文件名称： email_sender.py
# 项目描述： 发送邮件的模块

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict
from xiaoqiangclub.config.log_config import log


class EmailSender:
    @staticmethod
    async def send_email(subject: str, body: str, to_email: str, from_email: str, smtp_server: str, smtp_port: int,
                         smtp_user: str, smtp_password: str) -> bool:
        """
        发送邮件。

        :param subject: 邮件主题，字符串类型。
        :param body: 邮件内容，字符串类型。
        :param to_email: 收件人邮箱，字符串类型。
        :param from_email: 发件人邮箱，字符串类型。
        :param smtp_server: SMTP服务器地址，字符串类型。
        :param smtp_port: SMTP服务器端口，整数类型。
        :param smtp_user: SMTP用户名，字符串类型。
        :param smtp_password: SMTP密码，字符串类型。
        :return: 邮件发送成功返回 True，否则返回 False。
        """
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, to_email, msg.as_string())
            server.close()
            log.info("邮件发送成功")
            return True
        except Exception as e:
            log.error(f"邮件发送失败: {e}")
            return False

    @staticmethod
    async def send_email_with_config(config: Dict[str, Dict[str, str]], subject: str, body: str) -> bool:
        """
        使用配置文件发送邮件。

        :param config: 配置字典，字典类型，包含 email 的配置信息。
        :param subject: 邮件主题，字符串类型。
        :param body: 邮件内容，字符串类型。
        :return: 邮件发送成功返回 True，否则返回 False。
        """
        email_config = config['email']
        return await EmailSender.send_email(
            subject=subject,
            body=body,
            to_email=email_config['to_email'],
            from_email=email_config['from_email'],
            smtp_server=email_config['smtp_server'],
            smtp_port=email_config['smtp_port'],
            smtp_user=email_config['smtp_user'],
            smtp_password=email_config['smtp_password']
        )
