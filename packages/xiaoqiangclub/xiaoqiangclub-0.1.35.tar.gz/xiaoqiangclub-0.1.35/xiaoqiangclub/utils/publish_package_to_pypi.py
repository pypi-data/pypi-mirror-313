# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/12/6 14:46
# 文件名称： publish_package_to_pypi.py
# 项目描述： 发布包到PyPI
# 开发工具： PyCharm
import os
import sys
import shutil
from typing import (List, Optional, Union)
from xiaoqiangclub.config.log_config import log
from xiaoqiangclub.cmd.terminal_command_executor import run_command


def get_egg_info_directories() -> List[str]:
    """
    获取项目目录下所有 .egg-info 文件夹
    :return: 返回所有 .egg-info 文件夹路径的列表
    """
    egg_info_dirs = []
    for dir_name in os.listdir(os.getcwd()):
        if dir_name.endswith('.egg-info') and os.path.isdir(dir_name):
            egg_info_dirs.append(dir_name)
    return egg_info_dirs


def delete_directories(directories: Union[List[str], bool]) -> None:
    """
    删除指定的目录，如果目录参数为 True，则删除默认的目录列表。
    :param directories: 要删除的目录列表，可以是 bool 或 list。
    """
    if directories is True:
        directories = ['build', 'dist', *get_egg_info_directories()]

    if isinstance(directories, list):
        for directory in directories:
            if os.path.exists(directory):
                shutil.rmtree(directory)
                log.info(f"已删除目录: {directory}")
            else:
                log.warning(f"目录不存在: {directory}")
    else:
        log.error(f"无效的目录类型: {directories}")


def check_setup_directory() -> None:
    """
    检查当前工作目录是否包含 setup.py 文件。
    """
    if not os.path.exists('setup.py'):
        log.error("错误：此脚本需要在 setup.py 所在的目录中运行。")
        raise FileNotFoundError("无法找到 setup.py 文件。请确保在项目根目录运行该脚本。")


def check_required_modules():
    """
    检查是否安装必要的模块
    """
    required_modules = ['twine']
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            log.error(f"模块 {module} 未安装，请运行 `pip install {module}` 安装该模块。")
            sys.exit(1)


def publish_package_to_pypi(pypi_token: str, delete_dir_before_publish: Optional[Union[List[str], bool]] = False,
                            delete_dir_after_publish: Optional[Union[List[str], bool]] = False) -> None:
    """
    自动构建并发布包到PyPI
    :param pypi_token: PyPI的发布密钥（通常使用__token__）
    :param delete_dir_before_publish: 发布前要删除的目录列表，可以是 bool 或 list，默认为 False
    :param delete_dir_after_publish: 是否在发布成功后删除生成的目录，可以是 bool 或 list，默认为 False
    """
    check_setup_directory()  # 检查是否在 setup.py 所在的目录中运行
    check_required_modules()  # 在主函数中检查模块是否安装

    # 删除指定目录（如果提供了目录列表）
    if delete_dir_before_publish:
        delete_directories(delete_dir_before_publish)

    # 构建包
    command_build = 'python setup.py sdist bdist_wheel'
    run_command(command_build)

    # 上传到PyPI
    command_upload = f'twine upload dist/* -u __token__ -p {pypi_token}'
    run_command(command_upload)

    # 如果发布成功，并且指定了删除生成目录，则删除
    if delete_dir_after_publish:
        log.info("发布任务完成，开始删除生成的目录...")
        delete_directories(delete_dir_after_publish)  # 删除默认的目录
        log.info("生成的目录已删除。")
