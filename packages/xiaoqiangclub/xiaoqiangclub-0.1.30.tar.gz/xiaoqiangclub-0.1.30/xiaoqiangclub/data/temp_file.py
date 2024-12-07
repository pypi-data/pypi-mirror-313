# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/14
# 文件名称： temp_file.py
# 项目描述： 提供生成临时文件和目录的工具函数
# 开发工具： PyCharm
import os
import tempfile
from typing import Optional
from xiaoqiangclub import format_path
from xiaoqiangclub.config.log_config import log


def create_temp_file(suffix: Optional[str] = None, prefix: Optional[str] = None,
                     directory: Optional[str] = None, delete: bool = False,
                     **kwargs) -> str:
    """
    创建临时文件，确保创建在系统的临时文件夹内，且根据用户提供的 directory 参数创建相应子目录。

    :param suffix: 临时文件的后缀名，默认为空
    :param prefix: 临时文件的前缀
    :param directory: 临时文件存放的目录，默认为 None，表示使用系统默认的临时目录
    :param delete: 是否在文件关闭后自动删除文件，默认为 False
    :param kwargs: 其他额外的参数，可以传递给 tempfile.NamedTemporaryFile
    :return: 创建的临时文件路径
    """
    try:
        # 获取系统默认的临时目录
        temp_dir = tempfile.gettempdir()

        if directory is not None:
            # 如果用户提供了 directory 参数，将它视为相对于系统临时目录的子目录
            directory = os.path.join(temp_dir, directory.lstrip('/').lstrip('\\'))
            # 如果指定目录不存在，则创建它
            if not os.path.exists(directory):
                os.makedirs(directory)
            log.debug(f"指定的目录 {directory} 被创建或已经存在。")
        else:
            directory = temp_dir  # 如果没有指定，使用系统默认临时目录

        # 创建临时文件
        temp_file = tempfile.NamedTemporaryFile(suffix=suffix, prefix=prefix, dir=directory, delete=delete, **kwargs)
        log.info(f"成功创建临时文件: {temp_file.name}")

        # 将

        return temp_file.name
    except Exception as e:
        log.error(f"创建临时文件失败: {e}")
        raise


def create_temp_dir(prefix: Optional[str] = None, directory: Optional[str] = None, **kwargs) -> str:
    """
    创建临时目录，确保创建在系统的临时文件夹内，且根据用户提供的 directory 参数创建相应子目录。

    :param prefix: 临时目录的前缀
    :param directory: 临时目录存放的目录，默认为 None，表示使用系统默认的临时目录
    :param kwargs: 其他额外的参数，可以传递给 tempfile.mkdtemp
    :return: 创建的临时目录路径，目录需要手动删除。
    """
    try:
        # 获取系统默认的临时目录
        temp_dir = tempfile.gettempdir()

        if directory is not None:
            # 如果用户提供了 directory 参数，将它视为相对于系统临时目录的子目录
            directory = os.path.join(temp_dir, directory.lstrip('/').lstrip('\\'))
            # 如果指定目录不存在，则创建它
            if not os.path.exists(directory):
                os.makedirs(directory)
            log.info(f"指定的目录 {directory} 被创建或已经存在。")
        else:
            directory = temp_dir  # 如果没有指定，使用系统默认临时目录

        # 创建临时目录
        temp_dir_path = tempfile.mkdtemp(prefix=prefix, dir=directory, **kwargs)
        log.info(f"成功创建临时目录: {temp_dir_path}")

        return format_path(temp_dir_path)
    except Exception as e:
        log.error(f"创建临时目录失败: {e}")
        raise


def get_current_system_tempdir() -> str:
    """获取当前系统的临时目录"""
    return tempfile.gettempdir()
