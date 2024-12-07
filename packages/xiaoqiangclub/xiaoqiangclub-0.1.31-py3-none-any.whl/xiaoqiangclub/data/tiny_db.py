# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/1 17:52
# 文件名称： tiny_db.py
# 项目描述： tinydb模块封装
# 开发工具： PyCharm
import os
from tinydb import TinyDB, Query
from tinydb.operations import (delete, set)
from typing import List, Dict, Union, Optional
from xiaoqiangclub.config.log_config import log
from tinydb.storages import Storage
from xiaoqiangclub.data.file import (read_file, write_file)


class CustomJSONStorage(Storage):
    def __init__(self, path):
        self._path = path
        self._data = None

    def read(self):
        return read_file(self._path) or {}

    def write(self, data):
        write_file(self._path, data)


class TinyDBManager(TinyDB):
    def __init__(self, db_file: str = 'tiny_db.json', **kwargs) -> None:
        """
        tinydb 封装：https://tinydb.readthedocs.io/en/latest/index.html
        :param db_file: 数据库文件名，默认为'tiny_db.json'
        :param kwargs: 其他额外的 TinyDB 配置参数
        """
        log.debug(f"初始化 TinyDBManager，数据库文件: {db_file}")
        db_file = db_file.strip('.json') + '.json'
        self.db_file = db_file
        # 调用父类初始化方法，传递额外的配置参数
        super().__init__(db_file, storage=CustomJSONStorage, **kwargs)

    def insert_data(self, data: Union[Dict, List[Dict]], table_name: str = 'default',
                    skip_existing: bool = False) -> Optional[Union[str, List[str]]]:
        """
        向指定表中插入数据

        :param data: 要插入的数据，可以是单个字典或字典列表（用于批量插入）
        :param table_name: 表名，默认为'default'
        :param skip_existing: 是否跳过已存在的数据
        :return: 插入操作的文档 ID 列表
        """
        try:
            table = self.table(table_name)
            if isinstance(data, list):
                items_to_insert = []
                for item in data:
                    if skip_existing and self.__exists(item, table):
                        log.debug(f"数据已存在，跳过插入: {item}")
                        continue
                    items_to_insert.append(item)
                return table.insert_multiple(items_to_insert)
            else:
                if skip_existing and self.__exists(data, table):
                    log.debug(f"数据已存在，跳过插入: {data}")
                    return []
                return table.insert(data)
        except Exception as e:
            log.error(f"插入数据时出现错误 (表: {table_name}, 数据: {data}): {repr(e)}")
            return None

    def __exists(self, data: Dict, table: TinyDB) -> bool:
        """
        检查数据是否已存在于表中

        :param data: 要检查的字典数据
        :param table: TinyDB 表对象
        :return: 如果存在返回 True，否则返回 False
        """
        conditions = [getattr(Query(), key) == value for key, value in data.items()]
        combined_condition = self._combine_conditions(conditions)
        return table.search(combined_condition) != []

    def query(self, conditions: Dict, table_name: str = 'default', is_global: bool = False) -> Optional[List[Dict]]:
        """
        查询表中符合条件的数据

        :param conditions: 查询条件字典
        :param table_name: 表名，默认为'default'
        :param is_global: 是否查询整个数据库，默认为False，表示只查询指定表。当is_global为True时，table_name 将被忽略。
        :return: 符合条件的字典列表
        """
        log.debug(f"查询表 {table_name}，查询条件: {conditions}, 查询范围: {'整个数据库' if is_global else '指定表'}")
        try:
            if is_global:
                # 查询整个数据库
                results = []
                for table_name in self.tables():
                    table = self.table(table_name)
                    conditions_list = [getattr(Query(), key) == value for key, value in conditions.items()]
                    combined_condition = self._combine_conditions(conditions_list)
                    result = table.search(combined_condition)
                    results.extend(result)
                log.debug(f"查询结果: {results}")
                return results
            else:
                # 查询指定表
                table = self.table(table_name)
                conditions_list = [getattr(Query(), key) == value for key, value in conditions.items()]
                combined_condition = self._combine_conditions(conditions_list)
                result = table.search(combined_condition)
                log.debug(f"查询结果: {result}")
                return result
        except Exception as e:
            log.error(f"查询数据时出现错误: {repr(e)}")
            return None

    def update_data(self, query: Dict[str, str], new_data: Dict[str, str], table_name: Optional[str] = None,
                    overwrite: bool = False) -> Optional[List[int]]:
        """
        更新符合条件的数据

        :param query: 查询条件字典，键值对格式（如：{'name': 'Alice'}）
        :param new_data: 新的数据字典，用于更新的数据（如：{'age': 35}）
        :param table_name: 表名，默认为None，表示更新整个数据库中符合条件的数据
        :param overwrite: 是否完全覆盖数据，默认为False，只更新指定字段
        :return: 更新操作影响的文档 ID 列表
        """
        log.debug(f"更新操作，查询条件: {query}，新的数据: {new_data}, 表: {table_name}, 完全覆盖: {overwrite}")
        try:
            if table_name:
                # 更新指定表的数据
                table = self.table(table_name)
                conditions_list = [getattr(Query(), key) == value for key, value in query.items()]
                combined_condition = self._combine_conditions(conditions_list)
                result = self.__perform_update(table, combined_condition, new_data, overwrite)
                log.debug(f"更新成功，表 {table_name}，返回被更新的文档 ID: {result}")
                return result  # 返回的已经是列表，不需要再包装
            else:
                # 更新整个数据库中符合条件的数据
                updated_ids = []
                for table_name in self.tables():
                    table = self.table(table_name)
                    conditions_list = [getattr(Query(), key) == value for key, value in query.items()]
                    combined_condition = self._combine_conditions(conditions_list)
                    result = self.__perform_update(table, combined_condition, new_data, overwrite)
                    updated_ids.extend(result)  # 收集所有表更新的结果
                log.debug(f"更新成功，更新的文档 ID: {updated_ids}")
                return updated_ids
        except Exception as e:
            log.error(f"更新数据时出现错误: {repr(e)}")
            return None

    @staticmethod
    def __perform_update(table, combined_condition, new_data: Dict[str, str], overwrite: bool) -> List[int]:
        """
        执行具体更新操作，支持字典，并根据 overwrite 参数决定是否完全覆盖数据

        :param table: 目标表
        :param combined_condition: 查询条件，表示要更新的数据记录的条件
        :param new_data: 新的数据字典，用于更新的数据（如：{'age': 35}）
        :param overwrite: 是否完全覆盖数据，默认为False，只更新指定字段
        :return: 更新操作影响的文档 ID 列表
        """
        if overwrite:
            # 查找符合条件的所有文档
            existing_docs = table.search(combined_condition)
            updated_ids = []
            for doc in existing_docs:
                doc_id = doc.doc_id  # 获取原始文档的 doc_id

                # 更新现有字段
                for key in new_data:
                    table.update(set(key, new_data[key]), doc_ids=[doc_id])

                # 删除 new_data 中不存在的字段
                for key in list(doc.keys()):
                    if key not in new_data and key != 'doc_id':
                        table.update(delete(key), doc_ids=[doc_id])

                updated_ids.append(doc_id)

            return updated_ids  # 返回更新的文档 ID 列表
        else:
            # 如果不完全覆盖，只更新指定字段
            result = table.update(new_data, combined_condition)
            return [result] if isinstance(result, int) else result

    def delete_data(self, query: Dict = None, table_name: str = None, delete_table: str = None,
                    delete_file: bool = False) -> Optional[bool]:
        """
        删除符合条件的数据或删除整个表或数据库文件

        :param query: 查询条件字典
        :param table_name: 表名，默认为None，表示删除整个数据库的符合条件的数据
        :param delete_table: 如果不为None，删除指定的表
        :param delete_file: 是否删除数据库文件
        """
        log.debug(f"删除操作，表: {table_name}, 查询条件: {query}, 删除表: {delete_table}, 删除文件: {delete_file}")
        try:
            if delete_file:
                self.close_db()
                os.remove(self.db_file)
                log.debug(f"删除数据库文件: {self.db_file}")
                return True
            elif delete_table:
                if delete_table in self.tables():
                    self.drop_table(delete_table)
                    log.debug(f"删除表: {delete_table}")
                    return True
                else:
                    log.warning(f"表 {delete_table} 不存在")
                return None
            else:
                if table_name:
                    # 删除指定表的数据
                    table = self.table(table_name)
                    if query:
                        conditions_list = [getattr(Query(), key) == value for key, value in query.items()]
                        combined_condition = self._combine_conditions(conditions_list)
                        table.remove(combined_condition)
                        log.debug(f"删除符合条件的记录: {query}，表名: {table_name}")
                        return True
                    else:
                        raise ValueError("请提供查询条件 query 用于删除数据！")
                else:
                    # 删除整个数据库中符合条件的数据
                    for table_name in self.tables():
                        table = self.table(table_name)
                        if query:
                            conditions_list = [getattr(Query(), key) == value for key, value in query.items()]
                            combined_condition = self._combine_conditions(conditions_list)
                            table.remove(combined_condition)
                            log.debug(f"删除符合条件的记录: {query}，表名: {table_name}")
                        else:
                            raise ValueError("如果不删除表或文件，必须提供查询条件用于删除数据")
                    return True
        except Exception as e:
            log.error(f"删除操作时出现错误: {repr(e)}")
            return False

    def close_db(self) -> None:
        """
        关闭数据库连接
        """
        log.debug("关闭数据库连接...")
        try:
            self.close()
        except Exception as e:
            log.error(f"关闭数据库连接时出现错误: {repr(e)}")

    @staticmethod
    def _combine_conditions(conditions: List) -> Optional[Query]:
        if not conditions:
            return None
        combined_condition = conditions[0]
        for condition in conditions[1:]:
            combined_condition &= condition
        return combined_condition

    def get_all_data(self, table_name: Optional[str] = None) -> Optional[List[dict]]:
        """
        获取指定表格的所有数据，或者获取整个数据库的所有数据。

        :param table_name: 指定表名，如果为 None，则获取整个数据库的所有数据。
        :return: 返回所有数据的列表
        """
        if table_name:
            # 如果传入了表名，首先检查表是否存在
            if table_name not in self.tables():
                log.warning(f"表 {table_name} 不存在")
                return None
            table = self.table(table_name)
            return table.all()
        else:
            # 如果没有传入表名，则获取所有表的数据
            all_data = []
            for table_name in self.tables():
                table = self.table(table_name)
                all_data.extend(table.all())
            return all_data

    def __enter__(self):
        log.debug(f"打开数据库 {self.db_file} ...")
        return self  # 返回数据库对象，这样可以在 with 语句中使用 self

    # 通过 with 语句退出时会调用此方法
    def __exit__(self, exc_type, exc_val, exc_tb):
        log.debug(f"关闭数据库 {self.db_file}...")
        self.close_db()  # 确保数据库连接被关闭
