# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/27 6:13
# 文件名称： redis_manager.py
# 项目描述： Python操作Redis的简单封装
# 开发工具： PyCharm
import json
import re
from redis import Redis
# 从 aioredis.py  4.2.0rc1+ 开始，Aioredis 已经集成到 aioredis.py 中,并且 Aioredis 将不再更新维护，
# 导入：from redis import asyncio as aioredis (只有 2023 版本的 pycharm 才不会报错)
from redis import asyncio as aioredis
from typing import (Any, Optional, Tuple, List, Union)
from xiaoqiangclub.config.log_config import log


class RedisManager:
    def __init__(self,
                 host: Optional[str] = None,
                 port: Optional[int] = None,
                 password: Optional[str] = None,
                 db: int = 0,
                 redis_url: Optional[str] = None,
                 async_mode: bool = False):
        """
        Redis 管理器

        :param host: Redis 主机地址
        :param port: Redis 端口号
        :param password: Redis 密码
        :param db: Redis 数据库编号
        :param redis_url: Redis 连接 URL
        :param async_mode: 是否使用异步模式
        """
        self.async_mode = async_mode
        if redis_url:
            self.host, self.port, self.password, self.db = self.parse_redis_url(redis_url)
        else:
            self.host = host or 'localhost'
            self.port = port or 6379
            self.password = password
            self.db = db

        if async_mode:
            self.client = aioredis.Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                db=self.db
            )
        else:
            self.client = Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                db=self.db
            )

    @staticmethod
    def parse_redis_url(redis_url: str) -> Tuple[str, int, Optional[str], int]:
        """
        解析 Redis 连接 URL

        :param redis_url: Redis 连接 URL
        :return: (host, port, password, db)
        """
        try:
            regex = r'^(redis(?:s)?://)((?P<password>[^@]+)@)?(?P<host>[^:/]+)(:(?P<port>\d+))?(/(?P<db>\d+))?$'
            match = re.match(regex, redis_url)

            if not match:
                raise ValueError(f"无效的 Redis URL: {redis_url}")

            password = match.group('password')
            host = match.group('host')

            port_str = match.group('port')
            if port_str is not None:
                port = int(port_str)
            else:
                if match.group(0).startswith('redis://'):
                    port = 6379
                else:
                    port = 6380

            db_str = match.group('db')
            db = int(db_str) if db_str is not None else 0

            return host, port, password, db
        except Exception as e:
            log.error(f"解析 Redis URL 时出错: {e}")
            raise

    async def set_value_async(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """
        设置 Redis 中的值并可选择设置过期时间

        :param key: 键
        :param value: 值
        :param expire: 过期时间（秒），可选
        :return: 成功设置返回 True，否则返回 False
        """
        try:
            value = self._serialize(value)
            await self.client.set(key, value)
            if expire is not None:
                await self.client.expire(key, expire)
            log.debug(f"设置值: {key} = {value}, 过期时间: {expire}")
            return True
        except Exception as e:
            log.error(f"设置值时出错: {e}")
            return False

    def set_value(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """
        同步设置 Redis 中的值并可选择设置过期时间

        :param key: 键
        :param value: 值
        :param expire: 过期时间（秒），可选
        :return: 成功设置返回 True，否则返回 False
        """
        try:
            value = self._serialize(value)
            self.client.set(key, value)
            if expire is not None:
                self.client.expire(key, expire)
            log.debug(f"设置值: {key} = {value}, 过期时间: {expire}")
            return True
        except Exception as e:
            log.error(f"设置值时出错: {e}")
            return False

    async def get_value_async(self, key: str) -> Any:
        """
        获取 Redis 中的值

        :param key: 键
        :return: 值
        """
        try:
            value = await self.client.get(key)
            value = self._deserialize(value)
            log.debug(f"获取值: {key} = {value}")
            return value
        except Exception as e:
            log.error(f"获取值时出错: {e}")
            return None

    def get_value(self, key: str) -> Any:
        """
        同步获取 Redis 中的值

        :param key: 键
        :return: 值
        """
        try:
            value = self.client.get(key)
            value = self._deserialize(value)
            log.debug(f"获取值: {key} = {value}")
            return value
        except Exception as e:
            log.error(f"获取值时出错: {e}")
            return None

    async def delete_value_async(self, key: str) -> bool:
        """
        删除 Redis 中的值

        :param key: 键
        :return: 成功删除返回 True，否则返回 False
        """
        try:
            await self.client.delete(key)
            log.info(f"删除键: {key}")
            return True
        except Exception as e:
            log.error(f"删除键时出错: {e}")
            return False

    def delete_value(self, key: str) -> bool:
        """
        同步删除 Redis 中的值

        :param key: 键
        :return: 成功删除返回 True，否则返回 False
        """
        try:
            self.client.delete(key)
            log.info(f"删除键: {key}")
            return True
        except Exception as e:
            log.error(f"删除键时出错: {e}")
            return False

    async def key_exists_async(self, key: str) -> bool:
        """
        检查 Redis 中的键是否存在

        :param key: 键
        :return: 如果存在返回 True，否则返回 False
        """
        try:
            exists = await self.client.exists(key)
            log.debug(f"键 {key} 存在: {exists}")
            return exists > 0
        except Exception as e:
            log.error(f"检查键存在性时出错: {e}")
            return False

    def key_exists(self, key: str) -> bool:
        """
        同步检查 Redis 中的键是否存在

        :param key: 键
        :return: 如果存在返回 True，否则返回 False
        """
        try:
            exists = self.client.exists(key)
            log.debug(f"键 {key} 存在: {exists}")
            return exists > 0
        except Exception as e:
            log.error(f"检查键存在性时出错: {e}")
            return False

    async def get_expiration_async(self, key: str) -> Optional[int]:
        """
        获取 Redis 中键的过期时间

        :param key: 键
        :return: 过期时间（秒），如果不存在或没有设置过期时间返回 None
        """
        try:
            ttl = await self.client.ttl(key)
            log.info(f"键 {key} 的过期时间: {ttl}")
            return ttl
        except Exception as e:
            log.error(f"获取过期时间时出错: {e}")
            return None

    def get_expiration(self, key: str) -> Optional[int]:
        """
        同步获取 Redis 中键的过期时间

        :param key: 键
        :return: 过期时间（秒），如果不存在或没有设置过期时间返回 None
        """
        try:
            ttl = self.client.ttl(key)
            log.info(f"键 {key} 的过期时间: {ttl}")
            return ttl
        except Exception as e:
            log.error(f"获取过期时间时出错: {e}")
            return None

    async def fuzzy_search_async(self, pattern: str) -> List[str]:
        """
        使用模糊匹配查找 Redis 中的键

        :param pattern: 查找模式，支持通配符匹配。例如：'user:*' 将匹配所有以 "user:" 开头的键。
        :return: 匹配的键列表
        """
        try:
            cursor = 0
            matched_keys = []
            while True:
                cursor, partial_keys = await self.client.scan(cursor=cursor, match=pattern)  # 使用 scan 命令支持通配符
                matched_keys.extend([key.decode('utf-8') for key in partial_keys])
                if cursor == 0:  # cursor 为 0 时，扫描结束
                    break
            log.debug(f"模糊查找模式: {pattern}, 匹配的键: {matched_keys}")
            return matched_keys
        except Exception as e:
            log.error(f"模糊查找时出错: {e}")
            return []

    def fuzzy_search(self, pattern: str) -> List[str]:
        """
        使用模糊匹配查找 Redis 中的键

        :param pattern: 查找模式，支持通配符匹配。例如：'user:*' 将匹配所有以 "user:" 开头的键。
        :return: 匹配的键列表
        """
        try:
            cursor = 0
            matched_keys = []
            while True:
                cursor, partial_keys = self.client.scan(cursor=cursor, match=pattern)  # 使用 scan 命令支持通配符
                matched_keys.extend([key.decode('utf-8') for key in partial_keys])
                if cursor == 0:  # cursor 为 0 时，扫描结束
                    break
            log.debug(f"模糊查找模式: {pattern}, 匹配的键: {matched_keys}")
            return matched_keys
        except Exception as e:
            log.error(f"模糊查找时出错: {e}")
            return []

    async def regex_search_async(self, regex_pattern: str) -> List[str]:
        """
        使用正则表达式异步搜索 Redis 中的键

        :param regex_pattern: 正则表达式模式，用于匹配 Redis 中的键。
                              例如，若要匹配所有以 "user:" 开头的键，可以传入模式 "user:.*"。
                              该模式将会匹配所有以 "user:" 开头的键，后面跟任意字符。
                              需要注意的是，这里是一个正则表达式，因此支持多种复杂的模式匹配。

        :return: 匹配的键列表，返回所有匹配该正则表达式的键。
        """
        try:
            cursor = 0
            matched_keys = []
            while True:
                cursor, partial_keys = await self.client.scan(cursor=cursor, match='*')  # 使用 scan 替代 keys
                matched_keys.extend(
                    [key.decode('utf-8') for key in partial_keys if re.match(regex_pattern, key.decode('utf-8'))]
                )
                if cursor == 0:  # cursor 为 0 时，扫描结束
                    break
            log.debug(f"正则查找模式: {regex_pattern}, 匹配的键: {matched_keys}")
            return matched_keys
        except Exception as e:
            log.error(f"正则查找时出错: {e}")
            return []

    def regex_search(self, regex_pattern: str) -> List[str]:
        """
        使用正则表达式同步搜索 Redis 中的键

        :param regex_pattern: 正则表达式模式，用于匹配 Redis 中的键。
                              例如，若要匹配所有以 "user:" 开头的键，可以传入模式 "user:.*"。
                              该模式将会匹配所有以 "user:" 开头的键，后面跟任意字符。
                              需要注意的是，这里是一个正则表达式，因此支持多种复杂的模式匹配。

        :return: 匹配的键列表，返回所有匹配该正则表达式的键。
        """
        try:
            cursor = 0
            matched_keys = []
            while True:
                cursor, partial_keys = self.client.scan(cursor=cursor, match='*')  # 使用 scan 替代 keys
                matched_keys.extend(
                    [key.decode('utf-8') for key in partial_keys if re.match(regex_pattern, key.decode('utf-8'))]
                )
                if cursor == 0:  # cursor 为 0 时，扫描结束
                    break
            log.debug(f"正则查找模式: {regex_pattern}, 匹配的键: {matched_keys}")
            return matched_keys
        except Exception as e:
            log.error(f"正则查找时出错: {e}")
            return []

    async def set_key_persist_async(self, key: str) -> bool:
        """
        将指定的键设置为永不过期

        :param key: 键
        :return: 成功设置返回 True，否则返回 False
        """
        try:
            await self.client.persist(key)
            log.info(f"将键 {key} 设置为永不过期")
            return True
        except Exception as e:
            log.error(f"设置键 {key} 为永不过期时出错: {e}")
            return False

    def set_key_persist(self, key: str) -> bool:
        """
        将指定的键设置为永不过期

        :param key: 键
        :return: 成功设置返回 True，否则返回 False
        """
        try:
            self.client.persist(key)
            log.info(f"将键 {key} 设置为永不过期")
            return True
        except Exception as e:
            log.error(f"设置键 {key} 为永不过期时出错: {e}")
            return False

    def close(self):
        """关闭 Redis 连接"""
        try:
            self.client.close()
            self.client.connection_pool.disconnect()
            log.debug("同步 Redis 连接已关闭")
        except Exception as e:
            log.error(f"关闭 Redis 连接时出错: {e}")

    async def close_async(self):
        """异步关闭 Redis 连接"""
        try:
            await self.client.close()
            await self.client.connection_pool.disconnect()
            log.debug("异步 Redis 连接已关闭")
        except Exception as e:
            log.error(f"异步关闭 Redis 连接时出错: {e}")

    def __enter__(self):
        """同步上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """同步上下文管理器出口，关闭 Redis 连接"""
        if not self.async_mode:
            self.close()

    async def __aenter__(self):
        """异步上下文管理器入口"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口，关闭 Redis 连接"""
        if self.async_mode:
            await self.close_async()

    @staticmethod
    def _serialize(value: Any) -> str:
        """
        序列化值为 JSON 字符串

        :param value: 值
        :return: JSON 字符串
        """
        try:
            return json.dumps(value)
        except TypeError as e:
            log.error(f"序列化值时出错: {e}")
            raise

    @staticmethod
    def _deserialize(value: Union[bytes, str, None]) -> Any:
        """
        反序列化 JSON 字符串为原始值

        :param value: JSON 字符串
        :return: 原始值
        """
        if value is None:
            return None

        if isinstance(value, bytes):
            value = value.decode('utf-8')

        try:
            return json.loads(value)
        except json.JSONDecodeError as e:
            log.error(f"反序列化值时出错: {e}")
            raise
