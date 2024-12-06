# 文件名称： thread_runner.py
# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/12 07:12
# 项目描述： 在单独线程中运行指定的函数
# 开发工具： PyCharm
import inspect
import asyncio
from queue import Queue
from threading import Thread
from typing import Callable, Any, Tuple, Optional
from xiaoqiangclub.config.log_config import log


def run_in_thread(func: Callable[..., Any], return_result: bool = False,
                  daemon: bool = False, *args: Any, **kwargs: Any) -> Tuple[Thread, Optional[Queue]]:
    """
    在单独线程中运行指定的函数，并根据需要返回线程和队列以获取返回值。
    获取结果：
    ret = result_queue.get() if result_queue else None   # 阻塞式获取结果
    ret = result_queue.get_nowait() if result_queue else None   # 非阻塞式获取结果，请使用try-except语句处理异常，get_nowait()方法可能会导致程序崩溃。

    :param func: 需要在线程中运行的函数
    :param return_result: 是否需要返回结果队列
    :param daemon: 是否将线程设置为守护线程（和主线程一起退出）
    :param args: 函数的参数
    :param kwargs: 函数的关键字参数
    :return: 包含线程和可选队列的元组
    """
    result_queue = Queue() if return_result else None

    def thread_target():
        try:
            if inspect.iscoroutinefunction(func):  # 异步函数处理
                log.info(f"使用单独线程来执行异步函数：{func.__name__}...")
                loop = asyncio.new_event_loop()  # 创建新的事件循环
                asyncio.set_event_loop(loop)  # 设置为当前线程的事件循环
                result = loop.run_until_complete(func(*args, **kwargs))
            else:  # 同步函数处理
                log.info(f"使用单独线程来执行同步函数：{func.__name__}...")
                result = func(*args, **kwargs)

            if return_result:
                result_queue.put(result)  # 将结果放入队列
            log.info(f"{func.__name__} 执行结束！")
        except Exception as e:
            log.error(f"{func.__name__} 线程执行出错！", exc_info=True)
            if return_result:
                result_queue.put(e)  # 将错误放入队列

    thread = Thread(target=thread_target, name=f"Thread-{func.__name__}")
    thread.daemon = daemon  # 将线程设置为守护线程
    thread.start()
    return thread, result_queue
