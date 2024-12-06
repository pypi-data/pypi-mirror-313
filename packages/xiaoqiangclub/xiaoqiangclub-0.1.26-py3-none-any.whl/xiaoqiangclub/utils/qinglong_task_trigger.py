# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/7 16:42
# 文件名称： ql_task_trigger.py
# 项目描述： 配合青龙面板使用的任务触发器，青龙面板定时每20分钟或其他间隔，在指定的时间段内，每执行一次，就判断是否需要执行任务。
# 开发工具： PyCharm
import time
import inspect
from functools import wraps
from typing import Callable
from xiaoqiangclub.config.log_config import log


def minutes_to_time(minutes: int) -> str:
    """
    将分钟转换为时间格式（HH:MM），分钟数从00:00开始，不能超过1440分钟。

    :param minutes: 输入的分钟数，范围是0到1440之间。
    :return: 返回时间字符串，格式为"HH:MM"。
    :raises ValueError: 如果输入的分钟数不在有效范围内，抛出异常。
    """
    if not (0 <= minutes <= 1440):
        raise ValueError("分钟数必须在0到1440之间")

    hours = minutes // 60  # 计算小时
    minutes = minutes % 60  # 计算剩余的分钟

    return f"{hours:02}:{minutes:02}"  # 格式化输出为 HH:MM


def ql_task_trigger(total_runs_per_day: int, start_time: str = None, end_time: str = None,
                    main_program_start_interval: int = 20, skip_count: int = None,
                    valid_duration: int = 8, print_selected_times: bool = False, caller: str = None) -> bool:
    """
    判断是否需要执行任务，需配合青龙面板的间隔时间使用，例如 */20 * * * * 每20分钟执行一次，用于判断是否需要执行任务，
    考虑总次数、开始和结束时间、主程序启动间隔、任务有效期。

    :param total_runs_per_day: 一天需要执行的总次数
    :param start_time: 每天开始执行的时间，格式为 "HH:MM"，默认为 "00:00"
    :param end_time: 每天最晚结束的时间，格式为 "HH:MM"，默认为 "23:59"
    :param main_program_start_interval: 主程序的启动间隔，单位分钟，默认为20分钟
    :param skip_count: 当有效时间内主程序运行的次数大于total_runs_per_day的时候，跳过的执行次数，比如主程序在有效时间运行10次，而total_runs_per_day=2，interval_times=1，
    那么就可以在有效时间内，主程序运行的第1,3次返回True，如果次数不足，例如主程序在有效时间运行5次，而total_runs_per_day=4，interval_times=1，那么就可以在有效时间内，主程序运行的第1,3,4,5次返回True，默认为None,就直接连续的执行。
    :param valid_duration: 每次判定的有效时长（从主程序启动的时间开始计算），单位分钟，默认为5分钟，实际使用中要将程序的执行时间考虑进去
    :param print_selected_times: 是否打印选择的执行时间段，默认为False
    :param caller: 调用者，方便日志记录，默认为None
    :return: 是否需要执行任务的布尔值
    """
    caller = f'[{caller}]' if caller else ''

    # 校验 valid_duration 是否大于 main_program_start_interval
    if valid_duration > main_program_start_interval:
        raise ValueError(f"任务有效时间窗口 {valid_duration} 不能大于主程序的启动间隔 {main_program_start_interval}。")

    # 如果 start_time 或 end_time 为 None，设定为默认值
    start_time = start_time or "00:00"
    end_time = end_time or "23:59"

    # 计算执行的可用时间段（分钟）
    start_minutes = int(start_time.split(':')[0]) * 60 + int(start_time.split(':')[1])
    end_minutes = int(end_time.split(':')[0]) * 60 + int(end_time.split(':')[1])
    available_time = end_minutes - start_minutes

    # 校验总次数是否合法：判断 total_runs_per_day 是否超出可用时间段内能够完成的次数
    if total_runs_per_day > available_time // main_program_start_interval:
        raise ValueError(f"总次数 {total_runs_per_day} 超过了可用时间段内的执行次数限制。")

    # 获取当前时间的分钟数（从0点开始计算）
    current_time_minutes = (time.localtime().tm_hour * 60 + time.localtime().tm_min)

    # 判断当前时间是否在执行时间段内
    if not (start_minutes <= current_time_minutes <= end_minutes):
        return False  # 当前时间不在执行时间范围内

    # 计算主程序的执行时间段（每 main_program_start_interval 分钟从 00:00 开始）
    execution_times = []
    for i in range(0, 1440, main_program_start_interval):  # 一天的总分钟数1440
        if start_minutes <= i <= end_minutes:
            execution_times.append(i)

    if skip_count is None:  # 如果没有设置间隔次数，默认按顺序选择
        selected_times = execution_times[:total_runs_per_day]
    else:  # 如果 skip_count 存在（即我们要错开执行）
        selected_times = []
        i = 0
        while len(selected_times) < total_runs_per_day and i < len(execution_times):
            selected_times.append(execution_times[i])
            i += skip_count + 1  # 跳过 `skip_count` 次执行时间

        if len(selected_times) != total_runs_per_day:
            execution_times.reverse()
            for t in execution_times:
                if t not in selected_times:
                    selected_times.append(t)
                    if len(selected_times) == total_runs_per_day:
                        break

    # 从小到大排序
    selected_times.sort()

    # 将 selected_times 还原成时间字符串，方便日志记录
    selected_times_str = [
        f"{minutes_to_time(t)}-{minutes_to_time(t + valid_duration)}"
        for t in selected_times
    ]

    if print_selected_times:  # 打印选择的执行时间段
        print(selected_times_str)

    # 判断当前时间是否在选择的执行时间段内
    for execution_time in selected_times:
        # 判断当前时间是否在某个执行时间段内，同时还需检查有效时间窗口
        if execution_time <= current_time_minutes < execution_time + valid_duration:
            log.info(
                f"当前时间 {time.strftime('%H:%M', time.localtime())} {caller}在有效执行时间范围：{selected_times_str}，即将执行任务...")
            return True

    # 打印日志
    log.info(
        f"当前时间 {time.strftime('%H:%M', time.localtime())} {caller}不在有效执行时间范围：{selected_times_str}，跳过执行。")
    return False


