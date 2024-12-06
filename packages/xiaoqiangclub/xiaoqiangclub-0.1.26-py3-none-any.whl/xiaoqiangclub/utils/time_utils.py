# _*_ coding : UTF-8 _*_
# 开发人员： Xiaoqiang
# 开发时间： 2024/10/29
# 文件名称： time_utils.py
# 项目描述： 时间工具模块
from datetime import datetime


def get_current_time(use_chinese: bool = False) -> str:
    """
    获取当前时间。

    :param use_chinese: 是否使用中文格式，默认 False。
    :return: 格式化后的当前时间字符串。
    """
    formats = '%H时%M分%S秒' if use_chinese else '%H:%M:%S'
    return datetime.now().strftime(formats)


def __get_date_format(year_first: bool = True, show_year: bool = True, use_chinese: bool = False) -> str:
    """
    日期自定义格式

    :param year_first: 是否显示年份在前，默认为 True。
    :param show_year: 是否显示年份，默认为 True。
    :param use_chinese: 是否使用中文格式，默认 False。
    :return: 对应的日期格式字符串。
    """
    if use_chinese:
        if not show_year:
            return '%m月%d日'

        return '%Y年%m月%d日' if year_first else '%d月%d日%Y年'
    else:
        if not show_year:
            return '%m-%d'

        return '%Y-%m-%d' if year_first else '%m-%d-%Y'


def get_current_date(year_first: bool = True, show_year: bool = True, use_chinese: bool = False) -> str:
    """
    获取当前日期。

    :param year_first: 年份是否在前，默认为 True。
    :param show_year: 是否显示年份，默认为 True。
    :param use_chinese: 是否使用中文格式，默认 False。
    :return: 格式化后的当前日期字符串。
    """
    format_string = __get_date_format(year_first, show_year, use_chinese)
    return datetime.now().strftime(format_string)


def get_current_weekday(use_chinese: bool = False, short_form: bool = False) -> str:
    """
    获取当前星期几。

    :param use_chinese: 是否使用中文格式，默认 False。
    :param short_form: 是否使用简写形式，默认 False。
    :return: 当前星期的名称。
    """
    weekday_num = datetime.now().weekday()  # 0=Monday， 6=Sunday
    weekdays_en = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekdays_short_en = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    weekdays_cn = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期天']
    weekdays_short_cn = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

    if use_chinese:
        return weekdays_short_cn[weekday_num] if short_form else weekdays_cn[weekday_num]
    else:
        return weekdays_short_en[weekday_num] if short_form else weekdays_en[weekday_num]


def get_full_time_info(show_year: bool = True, year_first: bool = True,
                       show_weekday: bool = True, show_data: bool = True,
                       show_time: bool = True, use_chinese: bool = False,
                       separator: str = ' ', order: str = 'date-time-weekday') -> str:
    """
    获取当前时间、日期和星期的综合信息。

    :param show_year: 是否显示年份，默认为 True。
    :param year_first: 年份是否在前(日期中的位置)，默认为 True。
    :param show_weekday: 是否显示星期，默认 False。
    :param show_data: 是否显示日期，默认为 True。
    :param show_time: 是否显示时间，默认为 True。
    :param use_chinese: 是否使用中文格式，默认 False。
    :param separator: 各部分之间的分隔符，默认为空格。
    :param order: 显示顺序，支持 'date-time-weekday', 'date-weekday-time', 'weekday-date-time' 等。
    :return: 综合信息字符串。
    """
    time_string = get_current_time(use_chinese)
    date_string = get_current_date(year_first, show_year, use_chinese)
    weekday_string = get_current_weekday(use_chinese)

    result = []

    # 根据order参数排序
    for part in order.split('-'):
        if part == 'weekday' and show_weekday:
            result.append(weekday_string)
        elif part == 'date' and show_data:
            result.append(date_string)
        elif part == 'time' and show_time:
            result.append(time_string)

    return separator.join(result)


