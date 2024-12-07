# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/1 11:49
# 文件名称： text_splitter.py
# 项目描述： 分句：将一段文字分句
# 开发工具： PyCharm
import re
from typing import List


def text_splitter(s: str, keep_symbols=False, symbols_regex: str = None) -> List[str]:
    """
    将字符串按照指定的符号进行分句。

    :param s: 要分割的字符串。

    :param symbols_regex: 自定义句子分割符号。
    :param keep_symbols:：是否保留符号。
    :return: 分割后的列表。
    """
    symbols_regex = symbols_regex or r'[ ，。？！、…\n,.?!~]+'

    if keep_symbols:
        result_text = []
        symbols = []
        words = []
        for char in s:
            if re.match(symbols_regex, char):
                symbols.append(char)
            else:
                if symbols:
                    words.extend(symbols)
                    result_text.append(''.join(words))
                    symbols.clear()
                    words.clear()
                words.append(char)
        if words:
            words.extend(symbols)
            result_text.append(''.join(words))
        return [text for text in result_text if text.strip()]
    else:
        return [item.strip() for item in re.split(symbols_regex, s) if item.strip()]
