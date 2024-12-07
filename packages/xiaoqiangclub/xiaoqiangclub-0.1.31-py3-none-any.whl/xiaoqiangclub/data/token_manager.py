# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/8 11:24
# 文件名称： token_manager.py
# 项目描述： AccessToken/Token的时性管理工具，包括缓存、刷新和存储功能，支持同步和异步操作。
# 开发工具： PyCharm
import os
import json
import time
import asyncio
import aiofiles
from xiaoqiangclub.config.log_config import log
from typing import (Callable, Dict, Any, Optional, Awaitable)


class TokenManager:
    def __init__(self, fetch_token_fn: Callable[[], Dict[str, Any]],
                 storage_fn: Optional[Callable[[], Optional[Dict[str, Any]]]] = None, storage_path: str = None):
        """
        管理 Token 的时效性，包括缓存、刷新和存储功能
        用户可以通过继承并重写 refresh_token 和 save_token 方法来实现自定义的 token 刷新和存储逻辑

        :param fetch_token_fn: 用于获取新的 token 的函数该函数应该返回一个字典，包含 token 和 expires_at 字段
        :param storage_fn: 用于存储和加载 token 信息的函数默认是将 token 存储在内存中
        :param storage_path: 如果提供，将 token 存储到指定的文件路径如果为 None，则存储在内存中
        """
        self.fetch_token_fn = fetch_token_fn
        self.storage_path = storage_path

        # 默认的存储方式是内存存储，如果没有提供 storage_fn，则使用默认的存储
        self.storage_fn = storage_fn or (self._file_storage_fn if storage_path else self._default_storage_fn)

        self.token_data = None

    @staticmethod
    def _validate_token_data(token_data: dict) -> bool:
        """
        验证从 fetch_token_fn 获取的 token 数据格式

        :param token_data: 获取到的 token 数据
        :raises ValueError: 如果 token 数据不包含 expires_at 字段或其格式无效
        :return: True 表示数据格式正确，False 表示不正确
        """
        if 'token' not in token_data or 'expires_at' not in token_data:
            log.error("fetch_token_fn 返回的数据格式不正确：缺少 'token' 或 'expires_at' 字段")
            return False

        expires_at = token_data.get('expires_at')
        token = token_data.get('token')

        if not token:
            log.error("fetch_token_fn 返回的 token 字段为空！")
            return False
        if not expires_at:
            log.error("fetch_token_fn 返回的 expires_at 字段为空！")
            return False

        if not isinstance(expires_at, (int, float)):
            log.error("fetch_token_fn 返回的 expires_at 字段不是有效的时间戳！")
            return False

        return True

    def get_token(self) -> str:
        """
        获取有效的 token
        如果当前 token 过期，则刷新 token

        :return: 当前有效的 token
        """
        # 1. 从存储器加载 token 信息
        try:
            if not self.token_data:
                self.token_data = self.storage_fn()
        except Exception as e:
            log.error(f"加载 token 信息时出现错误：{e}将尝试获取新的 token")
            self.token_data = None

        # 2. 如果没有 token 信息，或者 token 过期，则刷新 token
        if not self.token_data or self._is_token_expired():
            log.info("token 已过期或不存在，正在刷新 token...")
            self.token_data = self.refresh_token()

        # 3. 返回有效的 token
        return self.token_data.get('token')

    def _is_token_expired(self) -> bool:
        """
        判断 token 是否过期

        :return: True 表示过期，False 表示有效
        """
        expires_at = self.token_data.get('expires_at')
        # 如果 expires_at 为 None，则认为 token 已过期
        if expires_at is None:
            return True
        # 使用 UNIX 时间戳进行比较
        return time.time() > expires_at

    def refresh_token(self) -> dict:
        """
        刷新 token
        通过调用 fetch_token_fn 获取新的 token，并计算过期时间，保存到存储中

        :return: 刷新后的 token 信息
        """
        try:
            # 1. 调用提供的函数获取新的 token
            new_token_data = self.fetch_token_fn()

            # 确保 token 数据有效
            if not self._validate_token_data(new_token_data):
                # 重新获取 token 数据
                new_token_data = self.fetch_token_fn()
                time.sleep(2)
                if not self._validate_token_data(new_token_data):
                    log.error("刷新 token 时出现错误：无法获取有效的 token 数据！")
                    return {}

            # 2. 保存新的 token 信息到存储器
            self.save_token(new_token_data)

            log.info(f"token 刷新成功新 token: {new_token_data['token']}")
            return new_token_data
        except Exception as e:
            log.error(f"刷新 token 时出现错误：{e}无法刷新 token")
            return {}

    def save_token(self, token_data: dict) -> None:
        """
        保存新的 token 信息可以重写此方法来自定义存储方式

        :param token_data: 包含 token 和 expires_at 的字典
        """
        try:
            self.storage_fn(token_data)
        except Exception as e:
            log.error(f"保存 token 信息时出现错误：{e}")

    def _default_storage_fn(self, token_data: Optional[dict] = None) -> Optional[dict]:
        """
        默认的存储器将 token 信息保存在内存中

        :param token_data: 要保存的 token 信息如果为 None，则返回存储的 token 信息
        :return: 当前存储的 token 信息
        """

        if token_data:
            # 将 token 保存到内存中
            self.__class__._default_storage_fn.token_data = token_data
            log.info("token 已保存到内存。")
            return None
        else:
            return getattr(self.__class__, '_default_storage_fn.token_data', None)

    def _file_storage_fn(self, token_data: Optional[dict] = None) -> Optional[dict]:
        """
        将 token 信息保存在指定的文件路径中

        :param token_data: 要保存的 token 信息如果为 None，则返回存储的 token 信息
        :return: 当前存储的 token 信息
        """
        if token_data:
            # 保存到文件
            if not self.storage_path:
                raise ValueError("存储路径不可为空，无法保存到文件")
            try:
                with open(self.storage_path, 'w') as file:
                    json.dump(token_data, file)
                log.info(f"token 已保存到文件：{self.storage_path}")
                return None
            except Exception as e:
                log.error(f"保存 token 到文件时出现错误：{e}")
                return None
        else:
            # 从文件中加载 token 信息
            if os.path.exists(self.storage_path):
                try:
                    with open(self.storage_path, 'r') as file:
                        return json.load(file)
                except Exception as e:
                    log.error(f"从文件加载 token 信息时出现错误：{e}")
                    return None
            return None


class TokenManagerAsync:
    def __init__(self, fetch_token_fn: Callable[[], Awaitable[Dict[str, Any]]],
                 storage_fn: Optional[Callable[[], Awaitable[Optional[Dict[str, Any]]]]] = None,
                 storage_path: str = None):
        """
        异步版本的 Token 管理器，用于管理 Token 的时效性，包括缓存、刷新和存储功能
        用户可以通过继承并重写 refresh_token 和 save_token 方法来实现自定义的 token 刷新和存储逻辑

        :param fetch_token_fn: 用于获取新的 token 的异步函数该函数应该返回一个字典，包含 token 和 expires_at 字段（Unix 时间戳，在什么时候过期）：{'token': 'xxxx', 'expires_at': 1234567890}
        :param storage_fn: 用于存储和加载 token 信息的异步函数默认是将 token 存储在内存中
        :param storage_path: 如果提供，将 token 存储到指定的文件路径如果为 None，则存储在内存中
        """
        self.fetch_token_fn = fetch_token_fn
        self.storage_path = storage_path

        # 默认的存储方式是内存存储，如果没有提供 storage_fn，则使用默认的存储
        self.storage_fn = storage_fn or (self._file_storage_fn if storage_path else self._default_storage_fn)

        self.token_data = None

    @staticmethod
    def _validate_token_data(token_data: dict) -> bool:
        """
        验证从 fetch_token_fn 获取的 token 数据格式

        :param token_data: 获取到的 token 数据
        :raises ValueError: 如果 token 数据不包含 expires_at 字段或其格式无效
        :return: True 表示数据格式正确，False 表示不正确
        """
        if 'token' not in token_data or 'expires_at' not in token_data:
            log.error("fetch_token_fn 返回的数据格式不正确：缺少 'token' 或 'expires_at' 字段")
            return False

        expires_at = token_data.get('expires_at')
        token = token_data.get('token')

        if not token:
            log.error("fetch_token_fn 返回的 token 字段为空！")
            return False
        if not expires_at:
            log.error("fetch_token_fn 返回的 expires_at 字段为空！")
            return False

        if not isinstance(expires_at, (int, float)):
            log.error("fetch_token_fn 返回的 expires_at 字段不是有效的时间戳！")
            return False

        return True

    async def get_token_async(self) -> str:
        """
        获取有效的 token如果当前 token 过期，则刷新 token

        :return: 当前有效的 token
        """
        # 1. 从存储器加载 token 信息
        try:
            if not self.token_data:
                self.token_data = await self.storage_fn()
        except Exception as e:
            log.error(f"加载 token 信息时出现错误：{e}将尝试获取新的 token")
            self.token_data = None

        # 2. 如果没有 token 信息，或者 token 过期，则刷新 token
        if not self.token_data or self._is_token_expired():
            log.info("token 已过期或不存在，正在刷新 token...")
            self.token_data = await self.refresh_token()

        # 3. 返回有效的 token
        return self.token_data.get('token')

    def _is_token_expired(self) -> bool:
        """
        判断 token 是否过期

        :return: True 表示过期，False 表示有效
        """
        expires_at = self.token_data.get('expires_at')
        if expires_at is None:
            return True
        return time.time() > expires_at

    async def refresh_token(self) -> dict:
        """
        刷新 token
        通过调用 fetch_token_fn 获取新的 token，并计算过期时间，保存到存储中

        :return: 刷新后的 token 信息
        """
        try:
            # 调用提供的异步函数获取新的 token
            new_token_data = await self.fetch_token_fn()

            # 确保 token 数据有效
            if not self._validate_token_data(new_token_data):
                # 重新获取 token 数据
                new_token_data = await self.fetch_token_fn()
                await asyncio.sleep(2)
                if not self._validate_token_data(new_token_data):
                    log.error("刷新 token 时出现错误：无法获取有效的 token 数据！")
                    return {}

            # 保存新的 token 信息到存储器
            await self.save_token(new_token_data)

            log.info(f"token 刷新成功新 token: {new_token_data['token']}")
            return new_token_data
        except Exception as e:
            log.error(f"刷新 token 时出现错误：{e}无法刷新 token")
            return {}

    async def save_token(self, token_data: dict) -> None:
        """
        保存新的 token 信息可以重写此方法来自定义存储方式

        :param token_data: 包含 token 和 expires_at 的字典
        """
        try:
            await self.storage_fn(token_data)
        except Exception as e:
            log.error(f"保存 token 信息时出现错误：{e}")

    async def _default_storage_fn(self, token_data: Optional[dict] = None) -> Optional[dict]:
        """
        默认的存储器将 token 信息保存在内存中

        :param token_data: 要保存的 token 信息如果为 None，则返回存储的 token 信息
        :return: 当前存储的 token 信息
        """
        if token_data:
            # 将 token 保存到内存中
            self.__class__._default_storage_fn.token_data = token_data
            log.info("token 已保存到内存。")
            return None
        else:
            return getattr(self.__class__, '_default_storage_fn.token_data', None)

    async def _file_storage_fn(self, token_data: Optional[dict] = None) -> Optional[dict]:
        """
        将 token 信息保存在指定的文件路径中

        :param token_data: 要保存的 token 信息如果为 None，则返回存储的 token 信息
        :return: 当前存储的 token 信息
        """
        if token_data:
            # 保存到文件
            if not self.storage_path:
                raise ValueError("存储路径不可为空，无法保存到文件")
            try:
                async with aiofiles.open(self.storage_path, 'w') as file:
                    await file.write(json.dumps(token_data))
                log.info(f"token 已保存到文件：{self.storage_path}")
                return None
            except Exception as e:
                log.error(f"保存 token 到文件时出现错误：{e}")
                return None
        else:
            # 从文件中加载 token 信息
            if os.path.exists(self.storage_path):
                try:
                    async with aiofiles.open(self.storage_path, 'r') as file:
                        token_data = await file.read()
                        return json.loads(token_data)
                except Exception as e:
                    log.error(f"从文件加载 token 信息时出现错误：{e}")
                    return None
            return None
