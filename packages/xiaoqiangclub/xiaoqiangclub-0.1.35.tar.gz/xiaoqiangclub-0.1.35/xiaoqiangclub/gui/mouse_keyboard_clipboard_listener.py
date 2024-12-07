# _*_ coding : UTF-8 _*_
# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2022/5/10  9:11
# 文件名称： mouse_keyboard_clipboard_listener.py
# 开发工具： PyCharm
import time
import pyperclip
import threading
from pynput import (mouse, keyboard)
from xiaoqiangclub.config.log_config import log
from typing import (Callable, Optional, List, Union)


class MouseKeyboardClipboardListener:
    def __init__(self, listen_name: str = 'MouseKeyboardClipboardListener'):
        """
        监听鼠标、键盘和剪贴板的变化
        官网文档：https://pynput.readthedocs.io/en/latest/

        :param listen_name: 给监听实例创建一个名字，用于辨认不同的监听实例
        """
        self.listen_name = listen_name
        self.mouse_listener = None
        self.keyboard_listener = None
        self.clipboard_thread = None
        self.hotkey_listener = None  # 用于存储热键监听器
        self.stop_event = threading.Event()  # 用于控制监听的停止事件
        self.stop_key = keyboard.Key.esc  # 默认停止键为Esc键

    def stop_keyboard_on_press(self, key):
        """
        键盘按下时的回调函数，判断是否按下自定义停止键。
        :param key: 按下的键
        :return: None
        """
        if key == self.stop_key:
            self.stop_all_listening()  # 直接调用停止监听方法

    @property
    def clipboard_data(self) -> str:
        """获取剪贴板数据"""
        return pyperclip.paste()

    def listen_clipboard_base(self, callback: Callable[[str], bool], interval: float = 0.5):
        """
        启动剪贴板监听的基础函数
        :param callback: 剪贴板变化时的回调函数，用户需要根据需求自行编写
        :param interval: 监听间隔，单位为秒
        """
        recent_data = self.clipboard_data
        while not self.stop_event.is_set():
            now_data = self.clipboard_data
            if now_data != recent_data:
                recent_data = now_data
                reply = callback(now_data)
                if not reply:
                    break
            time.sleep(interval)

    def start_listen_clipboard(self, on_change: Callable[[str], bool], interval: float = 0.5):
        """
        启动剪贴板监听，并在新线程中运行

        :param on_change: 剪贴板变化时的回调函数，用户需要根据需求自行编写
        :param interval: 监听间隔，单位为秒
        """
        self.clipboard_thread = threading.Thread(target=self.listen_clipboard_base, args=(on_change, interval))
        self.clipboard_thread.start()
        return self.clipboard_thread

    def start_listen_mouse(self, on_move: Optional[Callable] = None, on_click: Optional[Callable] = None,
                           on_scroll: Optional[Callable] = None):
        """
        启动鼠标监听，并在新线程中运行

        :param on_move: 鼠标移动时的回调函数，用户需要根据需求自行编写
        :param on_click: 鼠标点击时的回调函数，用户需要根据需求自行编写
        :param on_scroll: 鼠标滚动时的回调函数，用户需要根据需求自行编写
        """
        self.mouse_listener = mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll
        )
        self.mouse_listener.start()
        return self.mouse_listener

    def start_listen_keyboard(self, on_press: Optional[Callable] = None, on_release: Optional[Callable] = None,
                              stop_key: Optional[Union[str, keyboard.Key]] = keyboard.Key.esc):
        """
        启动键盘监听，并在新线程中运行

        :param on_press: 键盘按下时的回调函数，用户需要根据需求自行编写
        :param on_release: 键盘释放时的回调函数，用户需要根据需求自行编写
        :param stop_key: 自定义停止监听的按键，默认为Esc键
        """
        self.stop_key = stop_key
        self.keyboard_listener = keyboard.Listener(on_press=on_press or self.stop_keyboard_on_press,
                                                   on_release=on_release)
        self.keyboard_listener.start()
        return self.keyboard_listener

    def example_hotkey_callback(self):
        """示例热键回调函数，不需要参数，用户可以根据需求进行自定义"""
        log.info(f'{self.listen_name} -> 热键被触发！')

    def start_listen_hotkey(self, hotkeys: List[str], callback: Callable):
        """
        启动热键监听，用户只需提供热键的嵌套列表
        hotkeys = {
        "<ctrl>+<alt>+a": handle_hotkey_action,
        "<shift>+<alt>+b": handle_hotkey_action}

        :param hotkeys:快捷键列表，如['ctrl', 'shift', 'a']
        :param callback: 回调函数，用户需要根据需求自行编写
        """
        hot_key = ''
        for key in hotkeys[:-1]:
            hot_key += f'<{key}>+'
        hot_key += hotkeys[-1]

        self.hotkey_listener = keyboard.GlobalHotKeys({hot_key: callback})
        self.hotkey_listener.start()
        return self.hotkey_listener

    def stop_all_listening(self):
        """
        停止所有监听
        """
        self.stop_event.set()  # 设置停止事件
        if self.mouse_listener:
            self.mouse_listener.stop()  # 停止鼠标监听
            self.mouse_listener = None
        if self.keyboard_listener:
            self.keyboard_listener.stop()  # 停止键盘监听
            self.keyboard_listener = None
        if self.clipboard_thread:
            self.stop_event.set()  # 触发停止事件以停止剪贴板线程
            self.clipboard_thread.join()  # 等待剪贴板监听线程结束
            self.clipboard_thread = None
        if self.hotkey_listener:
            self.hotkey_listener.stop()  # 停止热键监听
            self.hotkey_listener = None
        log.info(f'{self.listen_name} -> 所有监听已停止')

    def stop_mouse_listener(self):
        """
        单独停止鼠标监听
        """
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None
            log.info(f'{self.listen_name} -> 鼠标监听已停止')

    def stop_keyboard_listener(self):
        """
        单独停止键盘监听
        """
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_listener = None
            log.info(f'{self.listen_name} -> 键盘监听已停止')

    def stop_clipboard_listener(self):
        """
        单独停止剪贴板监听
        """
        self.stop_event.set()  # 设置停止事件
        if self.clipboard_thread:
            self.clipboard_thread.join()  # 等待剪贴板监听线程结束
            self.clipboard_thread = None
            log.info(f'{self.listen_name} -> 剪贴板监听已停止')

    def stop_hotkey_listener(self):
        """
        停止热键监听
        """
        if self.hotkey_listener:
            self.hotkey_listener.stop()
            self.hotkey_listener = None
            log.info(f'{self.listen_name} -> 热键监听已停止')
