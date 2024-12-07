# _*_ coding : UTF-8 _*_
# 开发人员： XiaoqiangClub
# 微信公众号: XiaoqiangClub
# 开发时间：2024年06月13日
# 文件名称： config_loader.py
# 项目描述： 加载YAML和JSON配置文件的模块

import yaml
import json
from typing import Dict, Any


class ConfigLoader:
    @staticmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        """
        加载YAML或JSON配置文件

        :param config_path: 配置文件路径
        :return: 配置字典
        :raises FileNotFoundError: 当文件不存在时抛出异常
        :raises ValueError: 当文件格式不支持时抛出异常
        :raises Exception: 当文件读取或解析发生错误时抛出异常
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                    config = yaml.safe_load(file)
                elif config_path.endswith('.json'):
                    config = json.load(file)
                else:
                    raise ValueError("不支持的文件格式。请使用YAML或JSON文件。")
        except Exception as e:
            raise Exception(f"加载配置文件时发生错误：{e}")

        return config
