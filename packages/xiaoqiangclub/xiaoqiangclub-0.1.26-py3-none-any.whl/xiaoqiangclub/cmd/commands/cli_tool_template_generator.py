# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/3 11:35
# 文件名称： generate_cli_tool_template.py
# 项目描述： 生成命令行工具模板
# 开发工具： PyCharm
import os
import shutil
import argparse
from typing import Union
from xiaoqiangclub.config.constants import TEMPLATE_PATH


def generate_cli_tool_template(template_name: Union[str, argparse.Namespace],
                               output_dir: Union[str, argparse.Namespace] = None) -> None:
    """
    复制命令行工具模板文件到指定输出目录

    :param template_name: 模板名称，默认为 'cli_tool_template'
    :param output_dir: 输出目录，默认为当前目录
    """
    if isinstance(template_name, argparse.Namespace):
        output_dir = template_name.directory
        template_name = template_name.name.rstrip('.py')

    output_dir = output_dir or os.getcwd()

    if not os.path.exists(output_dir):
        raise ValueError("输出目录不存在")

    os.makedirs(output_dir, exist_ok=True)
    print(TEMPLATE_PATH)
    template_file = os.path.join(TEMPLATE_PATH, "cli_tool_template.py")
    if not os.path.exists(template_file):
        raise ValueError(f"模板文件 {template_file}不存在！")
    destination = os.path.join(output_dir, f"{template_name}.py")

    shutil.copy(template_file, destination)

    print(f"\n已生成命令行工具模板文件：{destination}\n")
