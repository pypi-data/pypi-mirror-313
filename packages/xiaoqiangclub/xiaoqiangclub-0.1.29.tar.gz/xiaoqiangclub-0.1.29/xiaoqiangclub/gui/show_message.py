# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/1 15:44
# 文件名称： show_message.py
# 项目描述： 消息弹窗
# 开发工具： PyCharm
import os
import base64
import threading
import tkinter as tk
from io import BytesIO
from PIL import Image, ImageTk
from tkinter import (messagebox, scrolledtext)
from typing import (Optional, Tuple, Union, List)
from xiaoqiangclub.config.log_config import log
from xiaoqiangclub.gui.logo import Base64Images  # 默认图标导入
from xiaoqiangclub.gui.play_system_sound import play_system_sound


def set_icon(window: tk.Tk, logo_path: str = None) -> None:
    """
    设置窗口图标。

    :param window: Tkinter窗口对象。
    :param logo_path: 图标的文件路径或Base64编码字符串，默认为默认图标。
    """
    if not logo_path:
        logo_path = Base64Images.logo_png
    try:
        if os.path.isfile(logo_path):
            # 使用Pillow加载图标
            img = Image.open(logo_path)
        else:
            # 处理可能是Base64编码的图标
            if logo_path.startswith('data:image/'):
                _, base64_data = logo_path.split(',', 1)
            else:
                base64_data = logo_path

            # 解码Base64数据并使用BytesIO
            image_data = base64.b64decode(base64_data)
            img = Image.open(BytesIO(image_data))

        img = img.convert("RGBA")
        img.thumbnail((64, 64), Image.LANCZOS)  # 使用LANCZOS重采样
        photo = ImageTk.PhotoImage(img, master=window)  # master参数用于指定图片所属的窗口
        window.iconphoto(False, photo)  # 设置图标
    except Exception as e:
        log.error(f"设置图标失败: {e}")  # 使用log.error()记录错误


def show_info(message: str, title: str = "消息", logo_path: str = Base64Images.logo_png) -> None:
    """
    显示信息弹窗。

    :param message: 弹窗内容，必须提供。
    :param title: 弹窗标题。
    :param logo_path: 图标的文件路径或Base64编码字符串，默认为默认图标。
    """
    window = tk.Tk()
    window.withdraw()  # 隐藏主窗口
    set_icon(window, logo_path)
    messagebox.showinfo(title, message)
    window.destroy()


def show_warning(message: str, title: str = "警告", logo_path: str = Base64Images.logo_png) -> None:
    """
    显示警告弹窗。

    :param message: 弹窗内容，必须提供。
    :param title: 弹窗标题。
    :param logo_path: 图标的文件路径或Base64编码字符串，默认为默认图标。
    """
    window = tk.Tk()
    window.withdraw()
    set_icon(window, logo_path)
    messagebox.showwarning(title, message)
    window.destroy()


def show_error(message: str, title: str = "错误", logo_path: str = Base64Images.logo_png) -> None:
    """
    显示错误弹窗。

    :param message: 弹窗内容，必须提供。
    :param title: 弹窗标题。
    :param logo_path: 图标的文件路径或Base64编码字符串，默认为默认图标。
    """
    window = tk.Tk()
    window.withdraw()
    set_icon(window, logo_path)
    messagebox.showerror(title, message)
    window.destroy()


def ask_question(message: str, title: str = "问题", logo_path: str = Base64Images.logo_png) -> bool:
    """
    显示问题弹窗并获取用户回答。

    :param message: 问题内容，必须提供。
    :param title: 弹窗标题。
    :param logo_path: 图标的文件路径或Base64编码字符串，默认为默认图标。
    :return: 用户的回答，返回True表示确认，返回False表示取消。
    """
    window = tk.Tk()
    window.withdraw()
    set_icon(window, logo_path)

    answer = messagebox.askyesno(title, message)  # 显示是/否选择框
    window.destroy()
    return answer


def show_input(prompt: str, title: str = '请输入', confirm_text: str = "确认", cancel_text: str = "取消",
               default_value: str = None, logo_path: str = Base64Images.logo_png, topmost: bool = True) -> str:
    """
    显示自定义输入对话框，允许用户输入文本。

    :param prompt: 提示文本
    :param title: 窗口标题
    :param logo_path: 窗口图标的文件路径或 Base64 编码字符串，默认为默认图标
    :param default_value: 输入框的默认值，默认为 None
    :param confirm_text: 确认按钮的文本，默认为 "确认"
    :param cancel_text: 取消按钮的文本，默认为 "取消"
    :param topmost: 是否将窗口置于最前，默认为 True
    :return: 用户输入的文本，如果取消则返回 None
    """

    # 创建主窗口
    root = tk.Tk()
    root.title(title)
    root.withdraw()  # 隐藏主窗口
    root.geometry("600x400")  # 固定窗口尺寸为 600x400

    # 设置窗口置顶
    if topmost:
        root.attributes("-topmost", True)

    # 设置窗口图标
    set_icon(root, logo_path)

    # 创建主框架
    main_frame = tk.Frame(root)
    main_frame.pack(padx=10, pady=20, fill=tk.BOTH, expand=True)

    # 创建可滚动的文本框
    prompt_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=10)
    prompt_text.insert(tk.END, prompt)
    prompt_text.config(state=tk.DISABLED)  # 禁用编辑
    prompt_text.pack(fill=tk.BOTH, expand=True)

    # 创建输入框
    entry = tk.Entry(main_frame, width=root.winfo_width())
    if default_value:
        entry.insert(0, default_value)
    entry.pack(pady=(10, 10))

    # 创建确认和取消按钮
    button_frame = tk.Frame(main_frame)
    button_frame.pack()

    confirm_button = tk.Button(button_frame, text=confirm_text, command=root.quit, width=10)
    confirm_button.pack(side=tk.LEFT, padx=10)
    cancel_button = tk.Button(button_frame, text=cancel_text, command=lambda: (entry.delete(0, tk.END), root.quit()),
                              width=10)
    cancel_button.pack(side=tk.LEFT, padx=10)

    root.protocol("WM_DELETE_WINDOW", lambda: (entry.delete(0, tk.END), root.quit()))  # 确保关闭窗口时也调用取消

    # 设置窗口最小尺寸
    root.minsize(600, 400)

    # 居中窗口
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 600) // 2
    y = (screen_height - 400) // 2
    root.geometry(f"600x400+{x}+{y}")

    # 显示窗口
    root.deiconify()

    # 运行窗口主循环
    root.mainloop()

    # 获取用户输入
    user_input = entry.get()
    return user_input if user_input else None


def get_position_coordinates(position: Optional[Union[str, Tuple[int], List[int]]],
                             width: int = 300, height: int = 100) -> Tuple[int, int]:
    """
    根据给定的位置信息计算窗口坐标。

    :param position: 位置信息，可以是预定义的字符串位置（如'top_left'等），也可以是包含两个整数的元组或列表表示坐标，或者为 None（默认居中）。
    :param width: 窗口宽度，默认为 300。
    :param height: 窗口高度，默认为 100。
    :return: 窗口的左上角坐标 (x, y)。
    """
    # 创建一个隐藏的主窗口来获取屏幕尺寸
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 如果传入的position是字符串类型的预定义位置
    if isinstance(position, str):
        if position == "top_left":
            return 8, 8
        elif position == "top_right":
            return screen_width - width - 16, 8
        elif position == "bottom_left":
            return 8, screen_height - height - 48
        elif position == "bottom_right":
            return screen_width - width - 16, screen_height - height - 48
        elif position == "center":
            return screen_width // 2 - width // 2, screen_height // 2 - height // 2

    # 如果传入的position是元组或列表，直接返回坐标
    if isinstance(position, (tuple, list)) and len(position) == 2:
        return position[0], position[1]

    # 默认居中位置
    return screen_width // 2 - width // 2, screen_height // 2 - height // 2


def _show_custom_info_thread(message, title, display_time, position, logo_path, min_size):
    """显示自定义信息窗口。"""
    root = tk.Tk()
    root.title(title)
    root.withdraw()
    root.resizable(False, False)
    # 置顶显示
    root.attributes("-topmost", True)

    set_icon(root, logo_path)

    label = tk.Label(root, text=message, wraplength=min_size[0] - 20)
    label.pack(fill=tk.BOTH, expand=True)

    root.update()
    window_width = min_size[0]
    window_height = min_size[1]
    while label.winfo_reqwidth() + 20 > window_width or label.winfo_reqheight() + 40 > window_height:
        window_width += 5
        window_height += 5
        if window_width > min_size[0] + 100 or window_height > min_size[1] + 100:
            break

    x, y = get_position_coordinates(position, window_width, window_height)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # 关闭窗口并继续执行后续代码
    def close_window():
        root.quit()  # 结束主循环
        root.destroy()  # 销毁窗口

    root.after(display_time, close_window)

    # 确保窗口关闭时也调用 close_window
    root.protocol("WM_DELETE_WINDOW", close_window)

    root.deiconify()

    root.mainloop()


def show_custom_info(message: str, title: str = '消息', display_time: int = 3000,
                     position: Optional[Union[str, Tuple[int], List[int]]] = "bottom_right",
                     logo_path: str = None, prompt_tone: bool = 'default',
                     min_size: Tuple[int, int] = (300, 100), use_thread: bool = True) -> None:
    """
    显示自定义信息窗口。

    :param message: 要显示的消息内容。
    :param title: 窗口标题，默认为'消息'。
    :param display_time: 窗口显示的时间（毫秒），默认为 3000。时间到后自动关闭窗口并退出程序。
    :param position: 窗口位置信息，可以是预定义的字符串位置（如'top_left'等），也可以是包含两个整数的元组或列表表示坐标，或者为 None（默认居中）。
    :param logo_path: 图标路径，可以是文件路径或 Base64 编码的图标数据。
    :param prompt_tone: 是否播放系统提示音。系统声音类型。Windows: 可选 'default', 'systemhand', 'exclamation', 'asterisk', 'question'。
                        macOS: 'default'。
    :param min_size: 窗口最小尺寸，默认为 (300, 100)，可以元组形式表示 (宽度, 高度)。
    :param use_thread: 是否使用单线程运行，默认为 True。注意：如果为 False，会阻塞主线程。
    """
    if logo_path is None:
        logo_path = Base64Images.logo_png

    # 播放系统提示音
    if prompt_tone:
        play_system_sound(prompt_tone)

    if use_thread:
        thread = threading.Thread(target=_show_custom_info_thread,
                                  args=(message, title, display_time, position, logo_path, min_size))
        thread.start()
    else:
        _show_custom_info_thread(message, title, display_time, position, logo_path, min_size)
