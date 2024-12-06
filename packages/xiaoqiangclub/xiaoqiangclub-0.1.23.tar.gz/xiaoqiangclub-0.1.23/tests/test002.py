# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024-11-15
# 文件名称： py
# 项目描述： 该模块用于处理csv和excel文件，实现对这些文件内容的增删改查功能，并支持同步和异步操作。
# 开发工具： PyCharm

from typing import List, Dict, Union
import csv
import pandas as pd
import asyncio
from xiaoqiangclub.config.log_config import log


# 同步读取CSV文件
def read_csv(file_path: str) -> List[Dict[str, Union[str, int, float]]]:
    """
    读取CSV文件内容。
    :param file_path: CSV文件路径
    :return: 返回一个字典列表，每个字典表示一行数据
    """
    log.info(f"开始读取CSV文件: {file_path}")
    data = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        log.info(f"成功读取{len(data)}条数据")
    except Exception as e:
        log.error(f"读取CSV文件失败: {e}")
    return data


# 同步写入CSV文件
def write_csv(file_path: str, data: List[Dict[str, Union[str, int, float]]]) -> bool:
    """
    将数据写入CSV文件。
    :param file_path: CSV文件路径
    :param data: 要写入的字典列表
    :return: 写入是否成功
    """
    log.info(f"开始写入数据到CSV文件: {file_path}")
    try:
        with open(file_path, mode='w', encoding='utf-8', newline='') as file:
            if data:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        log.info(f"成功写入{len(data)}条数据")
        return True
    except Exception as e:
        log.error(f"写入CSV文件失败: {e}")
        return False


# 同步读取Excel文件
def read_excel(file_path: str) -> pd.DataFrame:
    """
    读取Excel文件内容。
    :param file_path: Excel文件路径
    :return: 返回Pandas DataFrame，表示Excel数据
    """
    log.info(f"开始读取Excel文件: {file_path}")
    try:
        data = pd.read_excel(file_path)
        log.info(f"成功读取Excel文件，包含{len(data)}行数据")
        return data
    except Exception as e:
        log.error(f"读取Excel文件失败: {e}")
        return pd.DataFrame()


# 同步写入Excel文件
def write_excel(file_path: str, data: pd.DataFrame) -> bool:
    """
    将数据写入Excel文件。
    :param file_path: Excel文件路径
    :param data: 要写入的Pandas DataFrame
    :return: 写入是否成功
    """
    log.info(f"开始写入数据到Excel文件: {file_path}")
    try:
        data.to_excel(file_path, index=False)
        log.info(f"成功写入Excel文件")
        return True
    except Exception as e:
        log.error(f"写入Excel文件失败: {e}")
        return False


# 异步读取CSV文件
async def async_read_csv(file_path: str) -> List[Dict[str, Union[str, int, float]]]:
    """
    异步读取CSV文件内容。
    :param file_path: CSV文件路径
    :return: 返回一个字典列表，每个字典表示一行数据
    """
    log.info(f"开始异步读取CSV文件: {file_path}")
    data = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        log.info(f"成功异步读取{len(data)}条数据")
    except Exception as e:
        log.error(f"异步读取CSV文件失败: {e}")
    return data


# 异步写入CSV文件
async def async_write_csv(file_path: str, data: List[Dict[str, Union[str, int, float]]]) -> bool:
    """
    异步将数据写入CSV文件。
    :param file_path: CSV文件路径
    :param data: 要写入的字典列表
    :return: 写入是否成功
    """
    log.info(f"开始异步写入数据到CSV文件: {file_path}")
    try:
        with open(file_path, mode='w', encoding='utf-8', newline='') as file:
            if data:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        log.info(f"成功异步写入{len(data)}条数据")
        return True
    except Exception as e:
        log.error(f"异步写入CSV文件失败: {e}")
        return False


if __name__ == '__main__':
    def sync_example():
        csv_data = read_csv('example.csv')
        print("同步读取CSV数据：", csv_data)

        # new_data = [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}]
        # write_success = write_csv('new_example.csv', new_data)
        # print("同步写入CSV成功:", write_success)
        #
        # excel_data = read_excel('example.xlsx')
        # print("同步读取Excel数据：", excel_data)
        # 
        # excel_success = write_excel('new_example.xlsx', excel_data)
        # print("同步写入Excel成功:", excel_success)


    async def async_example():
        csv_data = await async_read_csv('example.csv')
        print("异步读取CSV数据：", csv_data)

        new_data = [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}]
        write_success = await async_write_csv('new_example.csv', new_data)
        print("异步写入CSV成功:", write_success)

        excel_data = await read_excel('example.xlsx')
        print("同步读取Excel数据：", excel_data)

        excel_success = write_excel('new_example.xlsx', excel_data)
        print("同步写入Excel成功:", excel_success)

        sync_example()
        # asyncio.run(async_example())
