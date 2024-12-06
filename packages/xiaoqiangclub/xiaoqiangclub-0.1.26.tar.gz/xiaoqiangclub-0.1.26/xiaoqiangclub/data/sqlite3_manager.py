# _*_ coding : UTF-8 _*_
# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2023/10/1 7:57
# 文件名称： sqlite3_manager.py
# 项目描述： SQLite数据库的同步异步增删改查API
# 开发工具： PyCharm
import sqlite3
import aiosqlite
from sqlitedict import SqliteDict
from xiaoqiangclub.config.log_config import log
from typing import (Any, Dict, List, Tuple, Optional)


class SQLite3DictManager:
    def __init__(self, db_path: str, table_name: str = "default", auto_commit: bool = True, **kwargs) -> None:
        """
        使用SqliteDict实现数据库管理

        :param db_path: 数据库文件路径
        :param table_name: 表名，默认为"default"
        :param auto_commit: 是否自动提交事务，默认为True
        """
        self.db_path = db_path
        self.table = table_name
        self.db: SqliteDict = None

        try:
            self.db = SqliteDict(db_path, tablename=table_name, autocommit=auto_commit, **kwargs)
            log.info(f"成功连接到数据库: {db_path}, 表: {table_name}")
        except Exception as e:
            log.error(f"连接到数据库时出错: {e}")
            raise

    def insert_data(self, key: str, value: Any) -> None:
        """
        插入数据

        :param key: 数据的键名
        :param value: 数据的值
        """
        self.db[key] = value
        log.info(f"插入数据: {key} -> {value}")

    def update_data(self, key: str, value: Any) -> None:
        """
        更新数据

        :param key: 数据的键名
        :param value: 更新后的值
        """
        if key in self.db:
            self.db[key] = value
            log.info(f"更新数据: {key} -> {value}")
        else:
            log.error(f"更新失败，键 {key} 不存在")

    def query_data(self, key: str) -> Any:
        """
        查询数据

        :param key: 数据的键名
        :return: 查询结果
        """
        value = self.db.get(key)
        log.info(f"查询结果: {key} -> {value}")
        return value

    def delete_data(self, key: str) -> None:
        """
        删除数据

        :param key: 数据的键名
        """
        if key in self.db:
            del self.db[key]
            log.info(f"删除数据: {key}")
        else:
            log.error(f"删除失败，键 {key} 不存在")

    def close(self) -> None:
        """关闭数据库连接"""
        if self.db:
            self.db.close()
            log.info("数据库连接已关闭")

    def __enter__(self):
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()
        log.info("数据库连接已关闭")


class SQLite3Manager:
    def __init__(self, db_path: str, is_async: bool = False):
        """
        初始化SQLite3Manager

        :param db_path: 数据库文件路径
        :param is_async: 是否使用异步连接
        """
        self.db_path = db_path
        self.is_async = is_async
        self.conn = None  # 连接

    async def connect_async(self) -> None:
        """异步连接到SQLite数据库"""
        try:
            self.conn = await aiosqlite.connect(self.db_path)
            log.info(f"成功异步连接到数据库: {self.db_path}")
        except Exception as e:
            log.error(f"异步数据库连接错误: {e}")

    def connect(self) -> None:
        """连接到SQLite数据库"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            log.info(f"成功连接到数据库: {self.db_path}")
        except Exception as e:
            log.error(f"数据库连接错误: {e}")

    def create_table(self, table_name: str, columns: Dict[str, str]) -> None:
        """
        创建表

        :param table_name: 表名
        :param columns: 列名和数据类型的字典
        """
        columns_definition = ", ".join([f"{col} {dtype}" for col, dtype in columns.items()])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition})"
        try:
            self.conn.execute(create_table_query)
            self.conn.commit()
            log.info(f"表 {table_name} 创建成功")
        except sqlite3.Error as e:
            log.error(f"创建表 {table_name} 时出错: {e}")

    async def create_table_async(self, table_name: str, columns: Dict[str, str]) -> None:
        """
        异步创建表

        :param table_name: 表名
        :param columns: 列名和数据类型的字典
        """
        columns_definition = ", ".join([f"{col} {dtype}" for col, dtype in columns.items()])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition})"
        try:
            await self.conn.execute(create_table_query)
            await self.conn.commit()
            log.info(f"异步表 {table_name} 创建成功")
        except Exception as e:
            log.error(f"异步创建表 {table_name} 时出错: {e}")

    def insert_data(self, table_name: str, data: Dict[str, Any]) -> None:
        """
        插入数据

        :param table_name: 表名
        :param data: 插入的数据字典
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        try:
            self.conn.execute(insert_query, tuple(data.values()))
            self.conn.commit()
            log.info(f"数据插入成功: {data}")
        except sqlite3.Error as e:
            log.error(f"插入数据时出错: {e}")

    async def insert_data_async(self, table_name: str, data: Dict[str, Any]) -> None:
        """
        异步插入数据

        :param table_name: 表名
        :param data: 插入的数据字典
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        try:
            await self.conn.execute(insert_query, tuple(data.values()))
            await self.conn.commit()
            log.info(f"异步数据插入成功: {data}")
        except Exception as e:
            log.error(f"异步插入数据时出错: {e}")

    def update_data(self, table_name: str, data: Dict[str, Any], condition: str) -> None:
        """
        更新数据

        :param table_name: 表名
        :param data: 更新的数据字典
        :param condition: 更新条件
        """
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        update_query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        try:
            self.conn.execute(update_query, tuple(data.values()))
            self.conn.commit()
            log.info(f"数据更新成功: {data}，条件: {condition}")
        except sqlite3.Error as e:
            log.error(f"更新数据时出错: {e}")

    async def update_data_async(self, table_name: str, data: Dict[str, Any], condition: str) -> None:
        """
        异步更新数据

        :param table_name: 表名
        :param data: 更新的数据字典
        :param condition: 更新条件
        """
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        update_query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        try:
            await self.conn.execute(update_query, tuple(data.values()))
            await self.conn.commit()
            log.info(f"异步数据更新成功: {data}，条件: {condition}")
        except Exception as e:
            log.error(f"异步更新数据时出错: {e}")

    def delete_data(self, table_name: str, condition: str) -> None:
        """
        删除数据

        :param table_name: 表名
        :param condition: 删除条件
        """
        delete_query = f"DELETE FROM {table_name} WHERE {condition}"
        try:
            self.conn.execute(delete_query)
            self.conn.commit()
            log.info(f"数据删除成功，条件: {condition}")
        except sqlite3.Error as e:
            log.error(f"删除数据时出错: {e}")

    async def delete_data_async(self, table_name: str, condition: str) -> None:
        """
        异步删除数据

        :param table_name: 表名
        :param condition: 删除条件
        """
        delete_query = f"DELETE FROM {table_name} WHERE {condition}"
        try:
            await self.conn.execute(delete_query)
            await self.conn.commit()
            log.info(f"异步数据删除成功，条件: {condition}")
        except Exception as e:
            log.error(f"异步删除数据时出错: {e}")

    def execute_query(self, table_name: str, condition: Optional[str] = None) -> List[Tuple[Any, ...]]:
        """
        执行查询并返回结果

        :param table_name: 表名
        :param condition: 查询条件（可选）
        :return: 查询结果
        """
        query = f"SELECT * FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        try:
            cursor = self.conn.execute(query)
            results = cursor.fetchall()
            log.info(f"查询成功: {results}")
            return results
        except sqlite3.Error as e:
            log.error(f"查询数据时出错: {e}")
            return []

    async def execute_query_async(self, table_name: str, condition: Optional[str] = None) -> List[Tuple[Any, ...]]:
        """
        异步执行查询并返回结果

        :param table_name: 表名
        :param condition: 查询条件（可选）
        :return: 查询结果
        """
        query = f"SELECT * FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        try:
            async with self.conn.execute(query) as cursor:
                results = await cursor.fetchall()
                log.info(f"异步查询成功: {results}")
                return results
        except Exception as e:
            log.error(f"异步查询数据时出错: {e}")
            return []

    def close(self) -> None:
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            log.info("数据库连接已关闭")

    async def close_async(self) -> None:
        """异步关闭数据库连接"""
        if self.conn:
            await self.conn.close()
            log.info("异步数据库连接已关闭")

    def __enter__(self):
        """上下文管理器入口"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()
        log.info('关闭数据库连接')

    async def __aenter__(self):
        """异步上下文管理器入口"""
        await self.connect_async()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.close_async()
        log.info('异步关闭数据库连接')
