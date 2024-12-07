# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/23 08:18
# 文件名称： fastapi_utils.py
# 项目描述： Fastapi工具包
# 开发工具： PyCharm
import json
import asyncio
from slowapi import Limiter
from fastapi import FastAPI, Request
from datetime import datetime, timedelta
from typing import Optional, Union, List
from slowapi.util import get_remote_address
from starlette.responses import JSONResponse
from xiaoqiangclub.config.log_config import log
from starlette.middleware.base import BaseHTTPMiddleware
from xiaoqiangclub.config.constants import SYSTEM_TEMP_DIR
from xiaoqiangclub.data.file import read_file_async, write_file_async


class SecurityMiddleware:
    def __init__(self, rate_limit: int, time_unit: str = "second", ban_on_rate_limit_exceed: bool = False,
                 ban_duration: Optional[int] = None, save_banned_ips: bool = False,
                 ban_file_path: Optional[str] = None, save_interval: int = 60):
        """
        初始化 SecurityMiddleware，集成速率限制和 IP 黑名单功能。

        :param rate_limit: 每个时间单位内允许的最大请求次数
        :param time_unit: 时间单位，例如 "second", "minute", "hour"
        :param ban_on_rate_limit_exceed: 是否在超过速率限制时封禁 IP
        :param ban_duration: 封禁时长，单位为分钟，None 表示永久封禁
        :param save_banned_ips: 是否保存封禁的 IP 到文件
        :param ban_file_path: 保存封禁 IP 的文件路径
        :param save_interval: 保存封禁 IP 的时间间隔，单位为秒
        """
        self.rate_limit = rate_limit
        self.time_unit = time_unit
        self.ban_on_rate_limit_exceed = ban_on_rate_limit_exceed
        self.ban_duration = ban_duration
        self.save_banned_ips = save_banned_ips
        self.ban_file_path = ban_file_path or f"{SYSTEM_TEMP_DIR}/fastapi_banned_ips.json" if save_banned_ips else None
        self.blocked_ips = {}

        # 初始化 Limiter
        self.limiter = Limiter(key_func=get_remote_address)
        self.save_interval = save_interval
        self._save_task = None

    async def initialize(self):
        """异步初始化，加载封禁的 IP 地址"""
        if self.save_banned_ips:
            await self.load_blocked_ips_from_file()

    async def clean_blocked_ips(self) -> None:
        """清理过期的封禁记录"""
        current_time = datetime.now().timestamp()
        for ip, ban_end_time in list(self.blocked_ips.items()):
            if ban_end_time != 0 and ban_end_time <= current_time:
                del self.blocked_ips[ip]

    async def save_blocked_ips_to_file(self) -> None:
        """将封禁的 IP 保存到文件"""
        try:
            if self.ban_file_path:
                await write_file_async(self.ban_file_path, json.dumps(self.blocked_ips))
                log.info(f"封禁的 IP 列表已保存到文件：{self.ban_file_path}")
        except Exception as e:
            log.error(f"保存封禁IP到文件时发生错误: {e}")

    async def load_blocked_ips_from_file(self) -> None:
        """从文件加载封禁的 IP 地址"""
        try:
            if self.ban_file_path:
                content = await read_file_async(self.ban_file_path)
                self.blocked_ips = json.loads(content) if content else {}
                log.debug(f"从 {self.ban_file_path} 加载封禁的 IP ...")
        except Exception as e:
            log.error(f"从文件加载封禁IP时发生错误: {e}")

    async def ban_ip(self, ip: Union[str, List[str]], duration: Optional[int] = None) -> None:
        """
        封禁单个或多个 IP 地址。

        :param ip: 要封禁的 IP 地址（可以是单个字符串或列表）
        :param duration: 封禁时长（分钟），None 表示永久封禁
        """
        if isinstance(ip, list):
            for single_ip in ip:
                self.blocked_ips[single_ip] = self._get_ban_end_time(duration)
        else:
            self.blocked_ips[ip] = self._get_ban_end_time(duration)

        # 在每次封禁之后，启动一个保存任务，但我们不立即写入文件，而是等一段时间批量写入
        if self.save_banned_ips and self._save_task is None:
            self._save_task = asyncio.create_task(self._schedule_save())

    @staticmethod
    def _get_ban_end_time(duration: Optional[int] = None) -> float:
        """计算封禁结束时间"""
        return 0 if duration is None else (datetime.now() + timedelta(minutes=duration)).timestamp()

    async def _schedule_save(self):
        """定期保存封禁 IP 列表到文件"""
        await asyncio.sleep(self.save_interval)
        await self.save_blocked_ips_to_file()
        self._save_task = None

    def rate_limit_decorator(self, rate_limit: Optional[int] = None, time_unit: Optional[str] = None):
        """
        返回速率限制的装饰器
        被 @rate_limit_decorator 装饰的函数或方法必须有 request: Request 参数
        注意：装饰器必须在路由函数之前使用（靠近函数）

        :param rate_limit: 每指定时间单位允许的最大请求次数
        :param time_unit: 时间单位，可选值为 "second"、"minute"、"hour"、"day"、"week"、"month"、"year"，默认为 "second"。可以在单位前面添加数字，如 "5 second" 表示每 5 秒允许 rate_limit 个请求。
        :return:
        """
        limit = rate_limit or self.rate_limit
        unit = time_unit or self.time_unit
        return self.limiter.limit(f"{limit}/{unit}")


class IPBlacklistMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, security_middleware: SecurityMiddleware):
        """
        FastAPI 中间件，用于检查 IP 是否被封禁。
        该中间件会检查每个请求的 IP 地址，若该 IP 地址在封禁列表中，则返回 403 Forbidden 错误。
        如果启用了封禁功能，当访问频率超过限制时，会封禁该 IP 地址。

        :param app: FastAPI 应用程序对象
        :param security_middleware: 用于检查请求是否包含有效的身份验证令牌的对象
        """
        super().__init__(app)
        self.security_middleware = security_middleware
        self.ban_ip_lock = asyncio.Lock()

    async def dispatch(self, request: Request, call_next):
        """
        处理每个请求，检查 IP 是否被封禁，并根据速率限制规则进行封禁操作。

        :param request: 请求对象
        :param call_next: 下一个中间件或请求处理函数
        :return: 请求处理后的响应
        """
        client_host = request.client.host

        # 清理过期封禁记录
        await self.security_middleware.clean_blocked_ips()

        # 如果 IP 被封禁，返回 403
        if client_host in self.security_middleware.blocked_ips:
            ban_end_time = self.security_middleware.blocked_ips[client_host]
            if ban_end_time == 0 or ban_end_time > datetime.now().timestamp():
                log.warning(f"IP {client_host} 被封禁，访问被拒绝...")
                return JSONResponse(status_code=403, content={"detail": "Forbidden"})

        # 处理请求
        response = await call_next(request)

        # 如果请求超出速率限制且需要封禁 IP
        if self.security_middleware.ban_on_rate_limit_exceed and response.status_code == 429:
            async with self.ban_ip_lock:
                await self.security_middleware.ban_ip(client_host, self.security_middleware.ban_duration)

        return response


def fastapi_ip_rate_limit_middleware(app: FastAPI,
                                     rate_limit: int, time_unit: str = "second",
                                     ban_on_rate_limit_exceed: bool = False,
                                     ban_duration: Optional[int] = None, save_banned_ips: bool = False,
                                     ban_file_path: Optional[str] = None, save_interval: int = 60) -> tuple:
    """
    集成速率限制和 IP 黑名单功能。
    被 @rate_limit_decorator 装饰的函数或方法必须有 request: Request 参数，装饰器必须在路由函数之前使用（靠近函数）

    :param app: FastAPI 应用实例
    :param rate_limit: 每分钟允许的最大请求次数
    :param time_unit: 时间单位，可选值为 "second"、"minute"、"hour"、"day"、"week"、"month"、"year"，默认为 "second"。可以在单位前面添加数字，如 "5 second" 表示每 5 秒允许 rate_limit 个请求。
    :param ban_on_rate_limit_exceed: 是否封禁 IP
    :param ban_duration: 封禁时长（分钟），None 表示永久封禁
    :param save_banned_ips: 是否保存封禁的 IP 到文件
    :param ban_file_path: 保存封禁 IP 的文件路径
    :param save_interval: 保存封禁 IP 的时间间隔（秒）
    :return: 返回速率限制装饰器 和 封禁 IP 的异步方法。注意：装饰器必须在路由函数之前使用（靠近函数）
    """
    # 将 Limiter 设置为 app.state.limiter
    app.state.limiter = Limiter(key_func=get_remote_address)

    security_middleware = SecurityMiddleware(
        rate_limit,
        time_unit,
        ban_on_rate_limit_exceed,
        ban_duration,
        save_banned_ips,
        ban_file_path,
        save_interval
    )
    app.add_middleware(IPBlacklistMiddleware, security_middleware=security_middleware)

    return security_middleware.rate_limit_decorator, security_middleware.ban_ip
