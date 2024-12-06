# _*_ coding: UTF-8 _*_
# 开发人员：Xiaoqiang
# 微信公众号: XiaoqiangClub
# 开发时间：2024/10/22
# 文件名称：windows_manager.py
# 项目描述：通过窗口标题获取窗口句柄，并进行窗口操作。
import win32gui
import win32con
from typing import Optional, List
from xiaoqiangclub.config.log_config import log


class WindowsManager:
    def __init__(self, title: Optional[str] = None):
        """
        窗口管理类，用于根据窗口标题获取窗口句柄，并执行一系列窗口操作。

        :param title: 窗口标题（支持模糊查找）
        """
        self.title = title
        self.hwnd: Optional[int] = None  # 当前窗口句柄

        if title:
            self.hwnd = self.find_window_by_title()

    def find_window_by_title(self, title: str = None) -> Optional[int]:
        """
        根据窗口标题查找窗口句柄。
        注意：如果浏览器有多个标签，只会识别当前活动标签的标题。

        :param title: 窗口标题（支持模糊查找）
        :return: 找到的窗口句柄，如果未找到则返回 None
        """
        title = title or self.title

        def enum_windows_callback(hwnd: int, results: List[int]):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if title.lower() in window_title.lower():  # 模糊查找
                    results.append(hwnd)

        hwnds = []
        win32gui.EnumWindows(enum_windows_callback, hwnds)

        return hwnds[0] if hwnds else None

    def window_is_maximized(self) -> Optional[bool]:
        """
        判断窗口是否最大化。
        :return:
        """
        try:
            placement = win32gui.GetWindowPlacement(self.hwnd)
            return placement[1] == win32con.SW_SHOWMAXIMIZED
        except Exception as e:
            log.error(f"判断窗口是否最大化失败: {e}")
            return None

    def minimize(self) -> Optional[int]:
        """最小化窗口。"""
        try:
            if self.hwnd and win32gui.IsWindow(self.hwnd):
                return win32gui.ShowWindow(self.hwnd, win32con.SW_MINIMIZE)
        except Exception as e:
            log.error(f"最小化窗口失败: {e}")

    def maximize(self) -> Optional[int]:
        """最大化窗口。"""
        try:
            if self.hwnd and win32gui.IsWindow(self.hwnd):
                return win32gui.ShowWindow(self.hwnd, win32con.SW_MAXIMIZE)
        except Exception as e:
            log.error(f"最大化窗口失败: {e}")

    def close(self) -> Optional[int]:
        """关闭窗口。"""
        try:
            if self.hwnd and win32gui.IsWindow(self.hwnd):
                return win32gui.PostMessage(self.hwnd, win32con.WM_CLOSE, 0, 0)
        except Exception as e:
            log.error(f"关闭窗口失败: {e}")

    def set_topmost(self) -> Optional[int]:
        """将窗口置顶。"""
        try:
            if self.hwnd and win32gui.IsWindow(self.hwnd):
                return win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                             win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        except Exception as e:
            log.error(f"设置窗口置顶失败: {e}")

    def remove_topmost(self) -> Optional[int]:
        """取消窗口的置顶状态。"""
        try:
            if self.hwnd and win32gui.IsWindow(self.hwnd):
                return win32gui.SetWindowPos(self.hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                             win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        except Exception as e:
            log.error(f"取消窗口置顶失败: {e}")

    def get_hwnd(self) -> Optional[int]:
        """获取当前窗口句柄。

        :return: 当前窗口句柄
        """
        return self.hwnd

    def set_window_handle(self, hwnd: int) -> None:
        """设置当前操作的窗口句柄。

        :param hwnd: 指定的窗口句柄
        """
        if win32gui.IsWindow(hwnd):
            self.hwnd = hwnd
        else:
            raise ValueError("提供的句柄无效或窗口不存在。")

    def set_window_title(self, title: str) -> None:
        """
        设置窗口标题

        :param title: 新窗口标题
        :return:
        """
        self.title = title
        self.hwnd = self.find_window_by_title(title)
