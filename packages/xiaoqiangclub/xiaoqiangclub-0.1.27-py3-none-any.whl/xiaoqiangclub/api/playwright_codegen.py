# _*_ coding: UTF-8 _*_
# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2023/10/6 14:51
# 文件名称： playwright_codegen.py
# 项目描述： 使用微软的playwright模块自动生成爬虫代码
# 开发工具： PyCharm
# 参考文章：https://xiaoqiangclub.blog.csdn.net/article/details/125201129
import os
import importlib
from urllib.parse import urlparse
from xiaoqiangclub.config.log_config import log
from xiaoqiangclub.cmd.module_installer import install_module
from xiaoqiangclub.cmd.terminal_command_executor import run_command


def install_playwright(browser: str = 'chromium') -> bool:
    """
    安装playwright及其浏览器驱动

    :param browser: 安装的浏览器，默认chromium，还有firefox，webkit和ffmpeg
    :return: 安装成功返回True，否则返回False
    """
    log.info("正在安装 playwright 模块...")

    if install_module("playwright"):
        log.info("playwright 安装成功，正在安装浏览器驱动...")
        ret = run_command(f"playwright install {browser}", stream_stdout=True)

        if ret:
            log.info(f"{browser} 驱动安装成功")
            return True
        else:
            log.error(f"{browser} 驱动安装失败")
            return False
    else:
        log.error("playwright 安装失败")
        return False


def __generate_file_path(url: str, directory: str = None) -> str:
    """
    生成代码文件路径

    :param url: 起始网站地址
    :param directory: 文件存放目录，默认为当前目录
    :return: 生成的文件路径
    """
    parsed_url = urlparse(url)
    domain = parsed_url.hostname.split('.')[1] if parsed_url.hostname else "default_code"
    directory = directory or os.getcwd()
    return os.path.join(directory, f"{domain}.py")


def playwright_codegen(url: str, file_name: str = None, proxy: str = None, directory: str = None) -> bool:
    """
    调用playwright生成Python浏览器爬虫代码
    https://xiaoqiangclub.blog.csdn.net/article/details/125201129

    :param url: 起始网站地址
    :param file_name: 生成的文件名.py，只需填写文件名即可，文件会自动生成到指定目录下
    :param proxy: 代理地址，如 http://192.168.1.111:7890
    :param directory: 文件存放目录，默认为当前目录
    :return: 执行结果输出，成功返回True，否则返回False
    """
    # 检查 playwright 模块是否安装
    try:
        importlib.import_module('playwright')
    except ImportError:
        log.warning("playwright 模块未安装")
        install = input("playwright 模块未安装，是否自动安装？(y/n): ").strip().lower()
        if install == 'y':
            if not install_playwright():
                log.error("playwright 安装失败，操作终止")
                return False
        else:
            log.error("playwright 模块未安装，操作终止")
            return False

    if not file_name:
        file_name = __generate_file_path(url, directory)

    command = f"playwright codegen --target python -o {file_name} -b chromium {url}"
    if proxy:
        command = f"playwright codegen --target python --proxy-server={proxy} -o {file_name} -b chromium {url}"

    log.info(f"生成代码命令: {command}")
    ret = run_command(command)

    if ret:
        log.info(f'代码生成成功：{file_name}')
        return True
    else:
        log.error('代码生成失败')
        return False
