# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/27 6:13
# 文件名称： file.py
# 项目描述： 常用文件的读写删等工具
# 开发工具： PyCharm
import os
import re
import yaml
import json
import aiofiles
from xiaoqiangclub.config.log_config import log
from typing import (Union, Optional, List, Tuple)


class FileFormatError(Exception):
    """自定义异常，表示文件格式不支持"""
    pass


def read_file(file_path: str, mode: str = 'r', encoding: str = 'utf-8',
              log_errors: bool = True, by_line: bool = False) -> any:
    """
    读取文件内容

    :param file_path: 文件路径
    :param mode: 读取模式，支持 'r' 或 'rb'
    :param encoding: 文件编码，默认为 'utf-8'
    :param log_errors: 是否记录错误日志，默认为 True
    :param by_line: 是否按行读取文件，默认为 False
    :return: 文件内容，格式根据文件类型返回不同类型
    """
    if not os.path.exists(file_path):
        log.error(f"文件 {file_path} 不存在！")
        return None

    try:
        if mode == 'r':
            with open(file_path, 'r', encoding=encoding) as file:
                if file_path.endswith('.json'):
                    return json.load(file)
                elif file_path.endswith(('.yaml', '.yml')):
                    return yaml.safe_load(file)
                elif file_path.endswith('.txt'):
                    if by_line:
                        return file.readlines()  # 按行读取
                    else:
                        return file.read()  # 整体读取
                else:
                    raise FileFormatError(f"不支持的文件格式: {file_path}")
        elif mode == 'rb':
            with open(file_path, 'rb') as file:
                return file.read()
        else:
            log.error(f"不支持的读取模式: {mode}")
            return None

    except Exception as e:
        log_errors and log.error(f"读取文件 {file_path} 时出错: {e}")
        return None


def write_file(file_path: str, data: Union[dict, str], mode: str = 'w', encoding: str = 'utf-8',
               ensure_ascii: bool = False, log_errors: bool = True, by_line: bool = False) -> Optional[bool]:
    """
    写入内容到文件，支持 'w'、'a'、'wb' 模式。

    :param file_path: 文件路径
    :param data: 要写入的内容，支持字符串或字典
    :param mode: 写入模式，支持 'w'、'a'、'wb'，默认为 'w'
    :param encoding: 文件编码，默认为 'utf-8'
    :param ensure_ascii: json 文件使用 ASCII 编码，默认为 False
    :param log_errors: 是否记录错误日志，默认为 True
    :param by_line: 是否按行写入文件，默认为 False
    :return: 是否写入成功
    """
    try:
        # 处理 'w'、'a' 和 'wb' 模式
        if mode in ['w', 'a']:  # 文本模式
            with open(file_path, mode=mode, encoding=encoding) as file:
                if file_path.endswith('.json'):
                    json.dump(data, file, ensure_ascii=ensure_ascii, indent=4)
                elif file_path.endswith(('.yaml', '.yml')):
                    yaml.dump(data, file, allow_unicode=True)
                else:
                    if by_line and isinstance(data, list):
                        file.writelines([line + "\n" for line in data])  # 按行写入
                    else:
                        file.write(data)
        elif mode == 'wb':  # 二进制模式
            with open(file_path, mode='wb') as file:
                file.write(data)
        else:
            log.error(f"不支持的写入模式: {mode}")
            raise FileFormatError(f"不支持的写入模式: {mode}")
        return True

    except Exception as e:
        if log_errors:
            log.error(f"写入文件 {file_path} 时出错: {e}")
        return False


async def read_file_async(file_path: str, mode: str = 'r', encoding: str = 'utf-8',
                          log_errors: bool = True, by_line: bool = False) -> any:
    """
    异步读取文件内容

    :param file_path: 文件路径
    :param mode: 读取模式，支持 'r' 或 'rb'
    :param encoding: 文件编码，默认为 'utf-8'
    :param log_errors: 是否记录错误日志，默认为 True
    :param by_line: 是否按行读取文件，默认为 False
    :return: 文件内容，格式根据文件类型返回不同类型
    """
    if not os.path.exists(file_path):
        log.error(f"文件 {file_path} 不存在！")
        return None

    try:
        if mode == 'r':
            async with aiofiles.open(file_path, mode='r', encoding=encoding) as file:
                if file_path.endswith('.json'):
                    content = await file.read()
                    return json.loads(content)
                elif file_path.endswith(('.yaml', '.yml')):
                    content = await file.read()
                    return yaml.safe_load(content)
                elif file_path.endswith('.txt'):
                    if by_line:
                        return [line async for line in file]  # 按行读取
                    else:
                        return await file.read()  # 整体读取
                else:
                    raise FileFormatError(f"不支持的文件格式: {file_path}")
        elif mode == 'rb':
            async with aiofiles.open(file_path, mode='rb') as file:
                return await file.read()
        else:
            log.error(f"不支持的读取模式: {mode}")
            raise FileFormatError(f"不支持的读取模式: {mode}")

    except Exception as e:
        log_errors and log.error(f"读取文件 {file_path} 时出错: {e}")
        return None


async def write_file_async(file_path: str, data: Union[dict, str], mode: str = 'w',
                           encoding: str = 'utf-8', ensure_ascii: bool = False,
                           log_errors: bool = True, by_line: bool = False) -> Optional[bool]:
    """
    异步写入内容到文件，支持 'w'、'a'、'wb' 模式。

    :param file_path: 文件路径
    :param data: 要写入的内容，支持字符串或字典
    :param mode: 写入模式，支持 'w'、'a'、'wb'，默认为 'w'
    :param encoding: 文件编码，默认为 'utf-8'
    :param ensure_ascii: json 文件使用 ASCII 编码，默认为 False
    :param log_errors: 是否记录错误日志，默认为 True
    :param by_line: 是否按行写入文件，默认为 False
    :return: 是否写入成功
    """
    try:
        # 处理 'w'、'a' 和 'wb' 模式
        if mode in ['w', 'a']:  # 文本模式
            async with aiofiles.open(file_path, mode=mode, encoding=encoding) as file:
                if file_path.endswith('.json'):
                    await file.write(json.dumps(data, ensure_ascii=ensure_ascii, indent=4))
                elif file_path.endswith(('.yaml', '.yml')):
                    await file.write(yaml.dump(data, allow_unicode=True))
                else:
                    if by_line and isinstance(data, list):
                        await file.writelines([line + "\n" for line in data])  # 按行写入
                    else:
                        await file.write(data)
        elif mode == 'wb':  # 二进制模式
            async with aiofiles.open(file_path, mode='wb') as file:
                await file.write(data)
        else:
            raise FileFormatError(f"不支持的写入模式: {mode}")
        return True

    except Exception as e:
        if log_errors:
            log.error(f"写入文件 {file_path} 时出错: {e}")
        return False


def delete_file(file_path: str) -> Optional[bool]:
    """
    删除指定文件

    :param file_path: 文件路径
    """
    if not os.path.exists(file_path):
        log.error(f"文件 {file_path} 不存在！")
        return None
    try:
        os.remove(file_path)
        log.info(f"成功删除文件: {file_path}")
        return True
    except Exception as e:
        log.error(f"删除文件 {file_path} 时出错: {e}")
        return False


def clean_filename(filename: str, extra_chars: Union[str, List[str]] = None, replacement: str = '') -> str:
    """
    清理文件名，去除特殊字符，包括反斜杠、正斜杠、冒号、星号、问号、双引号、小于号、大于号、管道符。

    :param filename: 原始文件名，类型为字符串。
    :param extra_chars: 可选参数，可以是一个字符串或者字符串列表，用于指定额外要从文件名中去除的字符。默认为 None。
    :param replacement: 可选参数，用于指定去除特殊字符后用什么字符来代替，默认为空字符串。
    :return: 优化后的文件名，类型为字符串。
    """
    invalid_chars = r'[\\/:*?"<>|]'
    if extra_chars:
        if isinstance(extra_chars, str):
            extra_chars = re.escape(extra_chars)
        elif isinstance(extra_chars, List):
            escaped_additional_chars = [re.escape(char) for char in extra_chars]
            extra_chars = '|'.join(escaped_additional_chars)
        invalid_chars += f'|{extra_chars}'
    return re.sub(invalid_chars, replacement, filename)


def format_path(path: str) -> str:
    """
    统一路径分隔符，将路径中的分隔符转换为当前操作系统默认的分隔符。

    :param path: 输入的路径字符串，可以包含多种路径分隔符。
    :return: 返回统一了分隔符后的路径。
    """
    # 获取当前操作系统的路径分隔符
    current_separator = os.sep

    # 如果是 Windows，当前分隔符是反斜杠，替换所有的正斜杠
    if current_separator == '\\':
        normalized_path = path.replace('/', '\\')
    else:
        # 如果是 Unix 系统（Linux/macOS），当前分隔符是正斜杠，替换所有的反斜杠
        normalized_path = path.replace('\\', '/')

    return normalized_path


def get_file_name_and_extension(file_path: str) -> Tuple[str, Optional[str]]:
    """
    提取文件/文件夹的文件名和后缀。

    :param file_path: str 文件/文件夹的路径
    :return: Tuple[str, Optional[str]] 返回文件名和后缀，文件夹时后缀为 None
    """

    return os.path.splitext(os.path.basename(file_path))
