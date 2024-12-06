# _*_ coding: UTF-8 _*_
# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/22 15:01
# 文件名称： module_installer.py
# 项目描述： python模块检测安装
# 开发工具： PyCharm
import sys
import importlib
import subprocess
from typing import List, Dict, Union
from xiaoqiangclub.config.log_config import log
from xiaoqiangclub.config.constants import PIP_MIRROR


def install_module(packages: Union[str, List[str]], mirror: str = PIP_MIRROR) -> bool:
    """
    安装指定的模块

    :param packages: 要安装的模块名称或模块名称列表
    :param mirror: 镜像地址（默认是阿里云镜像）
    :return: 所有模块安装是否成功
    """
    if isinstance(packages, str):
        packages = [packages]  # 如果是单个字符串，转换为列表

    package_list = ' '.join(packages)  # 将模块名称拼接成一个字符串
    log.info(f"正在安装 {package_list}...")

    try:
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '-i', mirror, '-U'] + packages
        )
        log.info(f"{package_list} 安装成功")
        return True
    except subprocess.CalledProcessError:
        log.error(f"安装 {package_list} 失败")
        return False


def check_and_install_module(module_mapping: Union[List[str], Dict[str, str]]):
    """
    检查并安装指定模块

    :param module_mapping: 模块名称列表或模块安装名称与导入名称的映射字典
                          - 如果是列表，列表中的每个模块名将作为安装名和导入名
                          - 如果是字典，字典的键是安装模块名称，值是导入模块名称
    """
    # 根据类型处理 module_mapping
    if isinstance(module_mapping, list):
        module_dict = {name: name for name in module_mapping}
    elif isinstance(module_mapping, dict):
        module_dict = module_mapping
    else:
        log.error("module_mapping 必须是列表或字典")
        return

    for install_name, import_name in module_dict.items():
        if not check_module(import_name):
            if install_module(install_name):
                log.info(f"模块 {import_name} 安装完毕")
            else:
                log.error(f"模块 {import_name} 安装失败，请手动安装")


def check_module(packages: Union[str, List[str]]) -> bool:
    """
    检查指定的模块是否已安装

    :param packages: 模块导入名称或模块名称列表
    :return: 所有模块检查是否成功
    """
    if isinstance(packages, str):
        packages = [packages]

    success = True
    for package in packages:
        try:
            importlib.import_module(package)
            log.info(f"{package} 已安装")
        except ImportError:
            log.error(f"{package} 未安装")
            success = False

    return success
