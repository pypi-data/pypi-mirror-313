# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/3 11:35
# 文件名称： create_docker_project.py
# 项目描述： 生成 Docker 项目模板
# 开发工具： PyCharm

import os
import shutil
import argparse
from typing import Union
from xiaoqiangclub.config.constants import TEMPLATE_PATH


def create_docker_project(args: Union[argparse.Namespace, dict]) -> None:
    """
    生成 Docker 项目模板，复制模板文件到指定的项目目录，并根据用户输入定制项目名称和路径。

    :param args: 包含项目名称和输出目录的参数，支持 argparse.Namespace 或字典形式
    """
    # 获取项目名称和输出目录
    if isinstance(args, argparse.Namespace):
        project_name = args.name
        output_dir = args.directory
    elif isinstance(args, dict):
        project_name = args.get("name", "xiaoqiangserver")  # 默认值改为 'xiaoqiangserver'
        output_dir = args.get("directory", os.getcwd())
    else:
        raise ValueError("参数类型不支持，仅支持 argparse.Namespace 或 dict 类型")

    # 设置模板文件源路径
    template_path = os.path.join(TEMPLATE_PATH, 'docker', project_name)

    # 检查模板路径是否存在
    if not os.path.exists(template_path):
        raise ValueError(f"模板路径 {template_path} 不存在，请确认模板文件夹位置。")

    output_dir = output_dir or os.getcwd()

    # 创建项目目录
    project_path = os.path.join(output_dir, project_name)
    if not os.path.exists(project_path):
        os.makedirs(project_path)
        print(f"创建项目目录: {project_path}")
    else:
        print(f"项目目录 {project_path} 已存在，跳过创建")

    # 复制模板文件到新项目目录
    try:
        for item in os.listdir(template_path):
            s = os.path.join(template_path, item)
            d = os.path.join(project_path, item)
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)

        print(f"\n项目模板已生成在: {project_path}\n")
    except Exception as e:
        raise ValueError(f"创建项目模板时发生错误: {e}")
