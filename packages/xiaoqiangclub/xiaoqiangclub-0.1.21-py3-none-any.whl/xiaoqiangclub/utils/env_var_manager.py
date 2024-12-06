# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/8 17:30
# 文件名称： env_var_manager.py
# 项目描述： 获取环境变量，设置环境变量，删除环境变量。
# 开发工具： PyCharm
import os
import platform
import subprocess
from typing import Optional
from xiaoqiangclub.config.log_config import log


def set_env_var(key: str, value: str, permanent: bool = False) -> None:
    """
    设置环境变量。

    :param key: str 环境变量的名称
    :param value: str 环境变量的值
    :param permanent: bool 是否设置为永久变量，默认值为 False
    :return: None
    """
    try:
        os.environ[key] = value
        if permanent:
            if platform.system() == 'Windows':
                subprocess.run(['setx', key, value], shell=True, check=True)
            else:
                # 在 Unix-like 系统上，设置永久环境变量需要添加到 shell 配置文件
                shell_config = os.path.expanduser('~/.bashrc')
                if platform.system() == 'Darwin':  # macOS
                    shell_config = os.path.expanduser('~/.zshrc')
                with open(shell_config, 'a') as file:
                    file.write(f'\nexport {key}={value}')
                log.info(f'永久环境变量 {key} 已添加到 {shell_config}，请手动运行 `source {shell_config}` 以使其生效')
    except Exception as e:
        log.error(f'设置环境变量 {key} 时发生错误: {e}')


def get_env_var(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    获取环境变量的值。

    :param key: str 环境变量的名称
    :param default: Optional[str] 如果环境变量不存在，则返回的默认值
    :return: Optional[str] 环境变量的值
    """
    try:
        return os.getenv(key, default)
    except Exception as e:
        log.error(f'获取环境变量 {key} 时发生错误: {e}')
        return default


def delete_env_var(key: str, permanent: bool = False) -> None:
    """
    删除环境变量
    windows系统下，只是删除临时变量，对于永久变量，需要手动删除。

    :param key: str 环境变量的名称
    :param permanent: bool 是否删除永久变量，默认值为 False
    :return: None
    """
    try:
        if key in os.environ:
            del os.environ[key]
        if permanent:
            if platform.system() == 'Windows':
                subprocess.run(['setx', key, ''], shell=True, check=True)
            else:
                shell_config = os.path.expanduser('~/.bashrc')
                if platform.system() == 'Darwin':  # macOS
                    shell_config = os.path.expanduser('~/.zshrc')

                # 修改文件时确保使用 UTF-8 编码
                with open(shell_config, 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                with open(shell_config, 'w', encoding='utf-8') as file:
                    for line in lines:
                        if f'export {key}=' not in line:
                            file.write(line)

                log.info(f'永久环境变量 {key} 已从 {shell_config} 中删除，请手动运行 `source {shell_config}` 以使其生效')
    except Exception as e:
        log.error(f'删除环境变量 {key} 时发生错误: {e}')


def load_env() -> None:
    """
    重新加载环境变量配置文件。

    :return: None
    """
    try:
        if platform.system() == 'Windows':
            subprocess.run(['cmd', '/c', 'set'], check=True)
        else:
            shell_config = os.path.expanduser('~/.bashrc')
            if platform.system() == 'Darwin':  # macOS
                shell_config = os.path.expanduser('~/.zshrc')
            subprocess.run(['source', shell_config], shell=True, check=True)
    except Exception as e:
        log.error(f'重新加载环境变量配置文件时发生错误: {e}')
