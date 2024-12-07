# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/1 11:49
# 文件名称： show_subtitles.py
# 项目描述： 显示字幕
# 开发工具： PyCharm
import time
import queue
import atexit
import threading
import tkinter as tk
import tkinter.font as tk_font
from typing import Optional, Union, Tuple
from xiaoqiangclub.config.log_config import log
from xiaoqiangclub.utils.text_splitter import text_splitter


class ShowSubtitles:
    def __init__(self, font_family: str = "Segoe UI", font_size: int = 24, font_color: str = "white",
                 bg_color: str = "black", bg_opacity: float = 0.8, position: Union[str, Tuple[int, int]] = "bottom",
                 duration: int = 3000, caption_width: Optional[int] = None, fade_in: bool = False,
                 fade_out: bool = True):
        """
        显示字幕
        :param font_family: 字体类型
        :param font_size: 字体大小
        :param font_color: 字体颜色
        :param bg_color: 背景颜色
        :param bg_opacity: 背景透明度（0.0到1.0）
        :param position: 字幕显示位置（bottom, top, left, right, center）或坐标元组 (x, y)
        :param duration: 字幕显示持续时间（毫秒）
        :param caption_width: 显示宽度（如果为 None，则使用屏幕宽度的2/3整数值）
        :param fade_in: 是否启用淡入效果
        :param fade_out: 是否启用淡出效果
        """
        self.font_family = font_family
        self.font_size = font_size
        self.font_color = font_color
        self.bg_color = bg_color
        self.bg_opacity = int(bg_opacity * 255)
        self.position = position
        self.duration = duration
        self.fade_in = fade_in
        self.fade_out = fade_out
        self.queue = queue.Queue()

        # 计算显示宽度，如果未指定则使用屏幕宽度的2/3
        self.caption_width = caption_width if caption_width is not None else int(self.get_screen_width() * 2 / 3)

        # 创建停止事件
        self.stop_event = threading.Event()

        # Tkinter 必须在主线程中运行，因此我们在新线程中创建 root
        self.tk_thread = threading.Thread(target=self.__run_tk, daemon=True)
        self.tk_thread.start()

        # 注册退出时的清理函数
        atexit.register(self.__close)

    @staticmethod
    def get_screen_width() -> int:
        """ 获取屏幕宽度 """
        root = tk.Tk()
        width = root.winfo_screenwidth()
        root.destroy()  # 关闭 Tkinter 根窗口
        return width

    def __run_tk(self) -> None:
        """ 运行 Tkinter 主循环 """
        self.root = tk.Tk()
        self.root.attributes('-alpha', 0.0)  # 初始时窗口全透明
        self.root.overrideredirect(True)  # 去除窗口边框
        self.root.attributes('-topmost', True)  # 确保窗口总是在最上层

        self.label = tk.Label(self.root, text="", font=(self.font_family, self.font_size), fg=self.font_color,
                              bg=self.bg_color, justify="center")
        self.label.pack(fill=tk.BOTH, expand=True)

        self.root.after(0, self.__process_queue)
        time.sleep(0.1)
        self.root.mainloop()

    def __close(self) -> None:
        """ 清理函数，用于关闭 Tkinter 窗口和结束线程 """
        self.stop_event.set()  # 设置停止事件
        if hasattr(self, 'root') and self.root.winfo_exists():  # 检查窗口是否存在
            self.root.after(0, self.__destroy_window)

    def __destroy_window(self) -> None:
        """ 在主线程中销毁窗口 """
        try:
            self.root.quit()  # 退出主循环
            self.root.destroy()  # 销毁窗口
        except tk.TclError:  # 如果窗口已销毁，则忽略错误
            pass

    def __process_queue(self) -> None:
        """ 处理消息队列 """
        if self.stop_event.is_set():  # 检查是否需要停止
            return
        try:
            if not self.queue.empty():
                message, duration = self.queue.get()
                self.__display_message(message, duration)
        except Exception as e:
            log.error(f"显示字幕失败: {e}")
        self.root.after(100, self.__process_queue)

    def __display_message(self, message: str, duration: int) -> None:
        """ 显示消息并设置定时隐藏 """
        # 更新标签文本
        self.label.config(text=message)

        # 重置标签大小和位置
        self.label.update_idletasks()
        self.__update_window_position(message)  # 传入消息以更新位置

        # 淡入新消息
        self.__fade_in()

        # 定时隐藏消息
        self.root.after(duration, self.__hide_message)

    def __fade_in(self) -> None:
        """ 实现淡入效果 """
        if not self.fade_in:  # 检查是否启用淡入效果
            self.root.attributes('-alpha', self.bg_opacity / 255)  # 直接设置最终透明度
            return

        self.root.attributes('-alpha', 0.0)
        step = self.bg_opacity // 100
        for i in range(0, self.bg_opacity + 1, step):
            self.root.attributes('-alpha', i / 255)
            self.root.update_idletasks()
            self.root.after(1)

    def __hide_message(self) -> None:
        """ 隐藏消息并检查队列 """
        self.__fade_out()
        self.root.after(0, self.__process_queue)  # 处理下一条消息

    def __fade_out(self) -> None:
        """ 实现淡出效果 """
        if not self.fade_out:  # 检查是否启用淡出效果
            self.root.attributes('-alpha', 0.0)  # 直接设置最终透明度
            return

        step = self.bg_opacity // 100
        for i in range(self.bg_opacity, -1, -step):
            self.root.attributes('-alpha', i / 255)
            self.root.update_idletasks()
            self.root.after(1)

    def __update_window_position(self, message: str) -> None:
        """ 更新窗口位置 """
        self.root.update_idletasks()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = self.caption_width  # 使用指定的显示宽度
        window_height = self.__calculate_window_height(message)  # 使用新方法计算高度

        if isinstance(self.position, tuple) and len(self.position) == 2:
            x, y = self.position
        else:
            if self.position == "bottom":
                x = (screen_width - window_width) // 2
                y = screen_height - window_height - 50
            elif self.position == "top":
                x = (screen_width - window_width) // 2
                y = 50
            elif self.position == "left":
                x = 50
                y = (screen_height - window_height) // 2
            elif self.position == "right":
                x = screen_width - window_width - 50
                y = (screen_height - window_height) // 2
            else:  # center
                x = (screen_width - window_width) // 2
                y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def __calculate_window_height(self, text: str) -> int:
        """ 计算窗口高度 """
        # 使用新方法获取行数
        lines, _ = self.__split_text_into_lines(text)
        font_obj = tk_font.Font(family=self.font_family, size=self.font_size)
        font_metrics = font_obj.metrics("linespace")  # 获取行高

        # 增加的上下边距
        padding = 20
        # 加上额外的行高，以确保每行文字完整显示
        return (font_metrics * lines) + padding  # 加上额外的行高

    @staticmethod
    def split_sentence_middle(sentence: str) -> Tuple[str, str]:
        """ 将一句话从中间切割成两部分，尽量从空格处分割 """
        # 去除句子两端的空格
        sentence = sentence.strip()

        # 计算句子的中间位置
        mid_index = len(sentence) // 2

        # 找到最近的空格作为分割点
        split_index = sentence.find(" ", mid_index)  # 从中间开始寻找空格

        if split_index == -1:  # 如果没有空格，直接从中间切割
            split_index = mid_index

        # 切割成两部分
        first_part = sentence[:split_index].strip()
        second_part = sentence[split_index:].strip()

        return first_part, second_part

    def __split_text_into_lines(self, text: str) -> Tuple[int, str]:
        """ 将文本拆分为多行，每行尽量显示完整的句子 """
        # 使用正则表达式分割句子，考虑各种标点符号
        sentences_list = text_splitter(text, keep_symbols=True)
        lines = []
        current_line = ""

        # 文字显示的最大宽度
        max_show_width = self.caption_width - 50
        # 创建字体对象以测量宽度
        font_obj = tk_font.Font(family=self.font_family, size=self.font_size)
        sentences = []

        # 将超过最大宽度的句子进行分句处理
        for sentence in sentences_list:
            if font_obj.measure(sentence) > max_show_width:
                first_part, second_part = self.split_sentence_middle(sentence)
                sentences.append(first_part)
                sentences.append(second_part)
            else:
                sentences.append(sentence)

        for sentence in sentences:
            # 计算当前行加上新句子的宽度
            test_line = f"{current_line} {sentence}".strip()
            width = font_obj.measure(test_line)

            if width <= max_show_width:  # 如果当前行宽度小于最大宽度（考虑内边距）
                current_line = test_line  # 更新当前行
            else:
                if current_line:  # 如果当前行不为空
                    lines.append(current_line)  # 将当前行添加到行列表中
                current_line = sentence.strip()  # 将当前句子设为新行的开始
        if current_line:  # 添加最后一行
            lines.append(current_line)  # 添加最后一行

        formatted_message = "\n".join(lines)  # 用换行符连接每一行
        return len(lines), formatted_message  # 返回行数和整理后的内容

    def show_subtitle(self, message: str, duration: Optional[int] = None) -> None:
        """
        显示消息
        :param message: 要显示的消息
        :param duration: 消息显示持续时间（毫秒），如果为 None，则使用默认持续时间
        """

        duration = duration or self.duration
        # 使用整理函数处理输入的消息
        while not hasattr(self, 'root'):
            log.debug('等待窗口初始化完成...')
            time.sleep(0.1)  # 等待 Tkinter 窗口初始化完成

        try:
            _, formatted_message = self.__split_text_into_lines(message)
            self.root.after(0, self.queue.put((formatted_message, duration)))
        except Exception as e:
            log.error(f"显示消息失败: {e}")
