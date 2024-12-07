# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/12/6 14:46
# 文件名称： publish_package_to_pypi.py
# 项目描述： 发布包到PyPI
# 开发工具： PyCharm
import os
import sys
import shutil
import subprocess
from typing import (List, Optional)
from xiaoqiangclub.config.log_config import log


def delete_directories(directories: List[str]) -> None:
    """
    删除指定的目录
    :param directories: 要删除的目录列表
    """
    for directory in directories:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            log.info(f"已删除目录: {directory}")
        else:
            log.warning(f"目录不存在: {directory}")


def run_command(command: str) -> None:
    """
    运行命令
    :param command: 要运行的命令
    """
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        log.info(f"命令成功: {command}")
        log.info(result.stdout)
    else:
        log.error(f"命令失败: {command}")
        log.error(result.stderr)


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


def publish_package_to_pypi(pypi_token: str, directories_to_delete: Optional[List[str]] = None) -> None:
    """
    自动构建并发布包到PyPI
    :param pypi_token: PyPI的发布密钥（通常使用__token__）
    :param directories_to_delete: 要删除的目录列表
    """
    check_required_modules()  # 在主函数中检查模块是否安装

    if directories_to_delete:
        # 删除指定的目录
        delete_directories(directories_to_delete)

    # 构建包
    command_build = 'python setup.py sdist bdist_wheel'
    run_command(command_build)

    # 上传到PyPI
    command_upload = f'twine upload dist/* -u __token__ -p {pypi_token}'
    run_command(command_upload)
