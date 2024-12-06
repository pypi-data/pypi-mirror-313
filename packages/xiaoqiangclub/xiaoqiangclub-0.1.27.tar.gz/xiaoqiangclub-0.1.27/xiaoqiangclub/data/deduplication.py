# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/31 17:50
# 文件名称： deduplication.py
# 项目描述： 爬虫去重，防止重复网址抓取
# 开发工具： PyCharm
import os
import time
import json
import hashlib
import aiofiles
from xiaoqiangclub.config.log_config import log
from typing import (Optional, Set, Any, List, Dict)


class Deduplication:
    """
    去重工具类，可以选择持久化已处理的任意数据。

    该类可用于在本地存储和管理已处理过的数据，以避免重复处理。通过设置持久化文件名，
    可以将已处理的数据保存到文件中，以便在程序下次运行时加载并继续使用。

    例如，可以用于爬虫程序中避免重复抓取相同的网页，也可以用于其他需要去重的场景。
    """

    def __init__(self, storage_file: Optional[str] = None, lazy_save: bool = False,
                 save_interval: Optional[int] = 30, save_count: Optional[int] = 10):
        """
        去重类，可以选择持久化已处理的数据。

        :param storage_file: 可选的持久化文件名，默认为 None，当设置时，会将已处理的数据持久化到该文件中。
        :param lazy_save: 是否采用懒惰保存策略，默认为 False。如果设置为 True，则 save_interval 和 save_count 参数生效。注意：为了防止数据丢失，请确保在程序退出前执行save_processed_data/save_async 方法，保存数据。
        :param save_interval: 懒惰保存时的自动保存时间间隔（以秒为单位），默认为 30 秒，表示不使用该功能。
        :param save_count: 懒惰保存时每添加多少条数据后自动保存，默认为 10，表示不使用该功能。
        """
        self.storage_file: Optional[str] = storage_file
        self.lazy_save: bool = lazy_save  # 是否采用懒惰保存策略
        self.save_interval: Optional[int] = save_interval if lazy_save else None  # 自动保存的时间间隔
        self.save_count: Optional[int] = save_count if lazy_save else None  # 自动保存的数据数量
        self.last_save_time: Optional[float] = time.time()  # 上次保存的时间
        self.data_added_since_last_save: int = 0  # 自上次保存以来添加的数据数量
        self.processed_data: Set[str] = set()  # 已处理的数据集合

        if self.storage_file:
            self.__load_processed_data()

    def __load_processed_data(self) -> None:
        """
        从文件中加载已处理的数据集合（如果设置了文件名）
        """
        if self.storage_file and os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    loaded_data = json.load(f)
                    self.processed_data = set(loaded_data)
            except (IOError, json.JSONDecodeError) as e:
                log.error(f"加载已处理数据时出现错误：{e}")

    @staticmethod
    def hash_data(data: Any) -> str:
        """
        使用 hashlib 生成数据的哈希值

        :param data: 要哈希的数据（可以是字符串或其他类型）
        :return: 数据的 MD5 哈希值
        """
        # 考虑使用更安全的哈希函数，如 sha256
        m = hashlib.md5()
        try:
            # 如果数据可以直接编码为字节，使用此方式
            m.update(data.encode('utf-8'))
        except AttributeError:
            # 如果数据不能直接编码，尝试转换为字符串后再编码
            m.update(str(data).encode('utf-8'))
        return m.hexdigest()

    def is_processed_data(self, data: Any) -> bool:
        """
        检查数据是否已处理

        :param data: 要检查的数据
        :return: 如果数据已处理，返回 True；否则返回 False
        """
        data_hash = self.hash_data(data)
        return data_hash in self.processed_data

    def add(self, data: Any) -> bool:
        """
        将数据添加到已处理的数据集合中

        :param data: 要添加的数据
        :return: 如果该数据是新的，返回 True；否则返回 False
        """
        data_hash = self.hash_data(data)
        if data_hash not in self.processed_data:
            self.processed_data.add(data_hash)

            # 仅在设置了 save_count 时进行计数
            if self.lazy_save and self.save_count:
                self.data_added_since_last_save += 1

            # 检查是否需要自动保存（仅在懒惰保存策略生效时）
            if self.lazy_save:
                if (self.save_interval and time.time() - self.last_save_time >= self.save_interval) or \
                        (self.save_count and self.data_added_since_last_save >= self.save_count):
                    self.save()
                    self.last_save_time = time.time()  # 更新上次保存时间
                    if self.save_count:
                        self.data_added_since_last_save = 0  # 重置计数器
            else:
                self.save()
            return True
        return False

    async def add_async(self, data: Any) -> bool:
        """
        将数据添加到已处理的数据集合中（异步接口）

        :param data: 要添加的数据
        :return: 如果该数据是新的，返回 True；否则返回 False
        """
        data_hash = self.hash_data(data)
        if data_hash not in self.processed_data:
            self.processed_data.add(data_hash)

            # 仅在设置了 save_count 时进行计数
            if self.lazy_save and self.save_count:
                self.data_added_since_last_save += 1

            # 检查是否需要自动保存（仅在懒惰保存策略生效时）
            if self.lazy_save:
                if (self.save_interval and time.time() - self.last_save_time >= self.save_interval) or \
                        (self.save_count and self.data_added_since_last_save >= self.save_count):
                    await self.save_async()  # 使用异步保存
                    self.last_save_time = time.time()  # 更新上次保存时间
                    if self.save_count:
                        self.data_added_since_last_save = 0  # 重置计数器
            else:
                await self.save_async()
            return True
        return False

    def save(self) -> None:
        """
        将已处理的数据集合保存到文件中（如果设置了文件名）
        """
        if self.storage_file:
            try:
                with open(self.storage_file, 'w') as f:
                    json.dump(list(self.processed_data), f)
            except IOError as e:
                log.error(f"保存已处理数据时出现错误：{e}")

    async def save_async(self) -> None:
        """
        将已处理的数据集合保存到文件中（如果设置了文件名）
        """
        if self.storage_file:
            try:
                async with aiofiles.open(self.storage_file, 'w') as f:
                    await f.write(json.dumps(list(self.processed_data)))
            except IOError as e:
                log.error(f"保存已处理数据时出现错误：{e}")

    def delete_data(self, data: Any) -> None:
        """
        同步删除已处理数据集合中的特定数据。

        :param data: 要删除的数据。
        """
        data_hash = self.hash_data(data)
        if data_hash in self.processed_data:
            self.processed_data.remove(data_hash)
            self.save()

    async def delete_data_async(self, data: Any) -> None:
        """
        异步删除已处理数据集合中的特定数据。

        :param data: 要删除的数据。
        """
        data_hash = self.hash_data(data)
        if data_hash in self.processed_data:
            self.processed_data.remove(data_hash)
            await self.save_async()

    def clear(self) -> None:
        """
        清空已处理的数据集合并删除持久化文件（如果存在）
        """
        self.processed_data.clear()
        if self.storage_file and os.path.exists(self.storage_file):
            os.remove(self.storage_file)

    def __enter__(self):
        return self

    async def __aenter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.save_async()


def dict_list_deduplicate(resource_list: List[Dict[str, Any]], key: str = None) -> List[Dict[str, Any]]:
    """
    字典列表去重

    :param resource_list: 需要去重的字典列表。
    :param key: 根据字典键名去重。如果为 None，字典去重。
    :return: 去重后的字典列表，保留第一次出现的每个键值对。
    """
    seen = set()  # 用于记录已出现的键值对（或者整个字典）
    unique_resources = []  # 用于存储去重后的字典列表

    for resource in resource_list:
        if key is None:
            # 如果没有指定 key，则根据整个字典去重
            resource_tuple = tuple(resource.items())  # 将字典转换为元组，方便去重
        else:
            # 否则根据指定的键去重
            resource_tuple = (resource.get(key),)

        if resource_tuple not in seen:  # 如果该键值对或字典还没有出现过
            seen.add(resource_tuple)  # 记录该键值对或字典
            unique_resources.append(resource)  # 添加到去重后的列表中

    return unique_resources
