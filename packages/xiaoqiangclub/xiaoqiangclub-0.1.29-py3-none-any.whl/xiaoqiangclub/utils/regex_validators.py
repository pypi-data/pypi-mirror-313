# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/3 10:07
# 文件名称： regex_validators.py
# 项目描述： 正则表达式验证器
# 开发工具： PyCharm
import re
from typing import (List, Optional)


class RegexValidator:
    """通用正则验证和提取模块"""

    # 定义正则表达式
    patterns = {
        'phone': r'(?:(?:\+?86)?(1[3-9]\d{9}))',  # 中国手机号码
        'email': r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+",  # 邮箱
        'url': r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"  # 网址
    }

    @staticmethod
    def validate(pattern_name: str, value: str) -> bool:
        """
        验证输入的值是否匹配给定的模式

        :param pattern_name: 模式名称
        :param value: 需要验证的字符串
        :return: 如果匹配返回 True，否则返回 False
        """
        pattern = RegexValidator.patterns.get(pattern_name)
        if pattern is None:
            raise ValueError(f"不支持的模式: {pattern_name}")

        try:
            return bool(re.fullmatch(pattern, value))
        except re.error as e:
            raise RuntimeError(f"正则表达式错误: {e}")

    @staticmethod
    def extract(pattern_name: str, text: str) -> Optional[List[str]]:
        """
        从输入的文本中提取匹配的值

        :param pattern_name: 模式名称
        :param text: 输入的字符串
        :return: 返回匹配的值列表，如果没有匹配则返回 None
        """
        pattern = RegexValidator.patterns.get(pattern_name)
        if pattern is None:
            raise ValueError(f"不支持的模式: {pattern_name}")

        try:
            matches = re.findall(pattern, text)
            return [match for match in matches] if matches else None
        except re.error as e:
            raise RuntimeError(f"正则表达式错误: {e}")
