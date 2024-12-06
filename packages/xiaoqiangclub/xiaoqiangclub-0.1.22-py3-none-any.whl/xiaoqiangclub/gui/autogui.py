# _*_ coding : UTF-8 _*_
# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/22 8:15
# 文件名称： autogui.py
# 项目描述： pyautogui桌面自动化
# 开发工具： PyCharm
import os
import time
import httpx
import pyperclip
import pyautogui
import webbrowser
from parsel import Selector
from typing import Optional
from pynput import keyboard
from xiaoqiangclub.config.log_config import log
from xiaoqiangclub.gui.show_subtitles import ShowSubtitles
from xiaoqiangclub.gui.show_message import show_custom_info
from xiaoqiangclub.gui.windows_manager import WindowsManager
from xiaoqiangclub.data.file import get_file_name_and_extension
from xiaoqiangclub.gui.mouse_keyboard_clipboard_listener import MouseKeyboardClipboardListener


class AutoGUI:
    def __init__(self, target: str = None, title: str = None, sleep_time: int = 1,
                 start_wait_time: int = 3, safe_mode: bool = False, show_subtitles: bool = True):
        """
        初始化 AutoGUI 类
        # 注意：这里需要安装 pip install -i https://pypi.doubanio.com/simple opencv-python Pillow pywin32

        :param target: 要打开的文件、程序或网址，可选参数
        :param title: 窗口标题，默认为None，如果未设置，程序会自动尝试获取。
        :param sleep_time: 每一步操作后等待的时间，默认为1秒
        :param start_wait_time: 等待程序启动的时间，默认为3秒，当auto_start为True时生效。
        :param safe_mode: 是否启用安全模式：按 Esc 键强制终止任务！默认为False，注意：当主程序正常运行结束后，监听程序需要手动按 Esc 停止！
        :param show_subtitles: 是否显示字幕，默认为True。当显示字幕的时候 show_message 的图标无法正常显示。
        """
        self.title = title
        self.target = target
        self.start_safe_mode = safe_mode

        # 设置pyautogui的操作间隔时间
        pyautogui.PAUSE = sleep_time
        self.open = self.start

        # 窗口管理
        self.windows_manager = WindowsManager()
        self.show_subtitles_listener = ShowSubtitles() if show_subtitles else None  # 显示字幕

        if self.target and self.target.startswith(('http://', 'https://')):
            self.title = title or self.get_url_title(self.target)
            # 打开网址
            webbrowser.open(self.target)
        elif self.target and os.path.exists(self.target):
            self.title = title or os.path.splitext(os.path.basename(self.target))[0]  # 使用文件名作为窗口标题
            os.startfile(self.target)
        else:
            log.info('未设置启动对象，如需启动对象，请手动调用 start 方法。')
            self.show_subtitle('未设置启动对象，如需启动对象，请手动调用 start 方法。')

        if target and start_wait_time > 0:
            time.sleep(start_wait_time)

        # 启动安全模式
        if safe_mode:
            log.info('已启用安全模式，按 Esc 键，可强制终止程序！')
            self.show_subtitle('已启用安全模式，按 Esc 键，可强制终止程序！')

            # 鼠标、键盘、剪贴板的监听对象
            self.listener = MouseKeyboardClipboardListener('AutoGUI')
            # 监听键盘
            self.listen_keyboard = self.listener.start_listen_keyboard(self.safe_mode)

    def show_subtitle(self, message: str):
        """显示字幕提示"""
        if self.show_subtitles_listener:
            self.show_subtitles_listener.show_subtitle(message)

    def safe_mode(self, key):
        """
        安全模式，当按下Esc键时，强制终止任务

        :param key:
        :return:
        """
        if key == keyboard.Key.esc:  # 键盘esc被释放，停止监听
            log.info('您按了 Esc 键，强制终止任务！')
            show_custom_info('您已强制终止任务！', '警告', display_time=1000, use_thread=False)
            # 取消置顶
            self.finish()

    def set_title(self, title: str):
        """
        设置窗口标题

        :param title: 窗口标题
        :return:
        """
        log.info(f'设置窗口标题为：{title}')
        self.title = title
        self.windows_manager.set_window_title(title)
        return self.title

    def start(self, target: Optional[str] = None, topmost: bool = False, maximize: bool = False,
              wait_image: Optional[str] = None, wait_time: int = 3):
        """
        打开文件、程序或网址，并设置窗口是否置顶和最大化

        :param target: 要打开的目标，如果未提供则使用初始化时的目标
        :param topmost: 是否置顶窗口
        :param maximize: 是否最大化窗口
        :param wait_image: 等待图片出现，如果出现就完成，否则等待 wait_time 秒
        :param wait_time: 等待窗口打开的时间（秒），默认为3秒
        """
        self.target = target or self.target
        if not self.target:
            log.warning('未提供目标，无法打开。')
            return None
        log.debug(f'打开 {self.target} ...')
        self.show_subtitle(f'打开 {self.target} ...')

        if self.target.startswith(('http://', 'https://')):
            if not self.title:
                return None
            # 打开网址
            webbrowser.open(self.target)
        elif os.path.exists(self.target):
            os.startfile(self.target)
        else:
            raise ValueError(f"无效的目标: {self.target}")

        if wait_time > 0:
            log.info(f'等待 {wait_time} 秒，等待窗口加载完成...')
            self.show_subtitle(f'等待 {wait_time} 秒，等待窗口加载完成...')
            time.sleep(wait_time)  # 等待窗口打开

        if wait_image:
            self.wait_for_image_to_appear(wait_image, wait_forever=True, auto_adjust_to_min_confidence=0.5,
                                          show_hint=True)
        if maximize:
            self.maximize_window()  # 最大化窗口
        if topmost:
            self.set_topmost()  # 置顶窗口

    def set_topmost(self):
        """
        设置窗口置顶
        """
        if not self.title:
            log.warning(f'未获取到 {self.target} 的标题！')
            return None
        log.info(f'设置 {self.title} 置顶...')
        self.show_subtitle(f'设置 {self.title} 置顶...')

        # 窗口置顶
        self.windows_manager.set_window_title(self.title)
        self.windows_manager.set_topmost()

    def cancel_topmost(self):
        """
        取消窗口置顶
        """
        if not self.title:
            log.warning(f'未获取到 {self.target} 的标题！')
            return None
        log.info(f'取消 {self.title} 置顶...')
        self.show_subtitle(f'取消 {self.title} 置顶...')
        self.windows_manager.set_window_title(self.title)
        self.windows_manager.remove_topmost()

    def maximize_window(self):
        """
        最大化窗口
        """

        if not self.title:
            log.warning(f'未获取到 {self.target} 的标题！')
            return None

        log.info(f'最大化 {self.title}...')
        self.show_subtitle(f'最大化 {self.title}...')
        self.windows_manager.set_window_title(self.title)

        if self.windows_manager.window_is_maximized() is True:
            log.info(f'{self.title} 已经最大化！')
            self.show_subtitle(f'{self.title} 已经最大化！')
            return None

        if not self.windows_manager.maximize():
            # 使用快捷键
            pyautogui.hotkey('win', 'up')

    def close_window(self, delay: int = 5):
        """
        关闭窗口

        :param delay: 延迟关闭窗口的时间（秒）
        """
        if not self.title:
            log.warning(f'未获取到 {self.target} 的标题！')
            return None
        log.info(f'关闭 {self.title}...')
        self.show_subtitle(f'关闭 {self.title}...')
        if delay > 0:
            time.sleep(delay)
        self.windows_manager.set_window_title(self.title)
        self.windows_manager.close()

    @staticmethod
    def get_image_center_pos(image_path: str, **kwargs) -> Optional[tuple]:
        """
        获取图像中心位置

        :param image_path: 图像路径
        :param kwargs: pyautogui.locateCenterOnScreen的参数
        :return:
        """
        try:
            return pyautogui.locateCenterOnScreen(image=image_path, **kwargs)
        except Exception as e:
            log.debug(f'获取图像中心位置失败：{e}')
            return None

    def search_image(self, image_path: str, click_left: bool = True, clicks: int = 1,
                     click_offset_x: int = 0, click_offset_y: int = 0, not_click: bool = False,
                     grayscale: bool = False, confidence: float = 0.7, auto_adjust_to_min_confidence: float = None,
                     fail_out: bool = False, timeout: int = None, wait_forever: bool = False,
                     **kwargs) -> Optional[tuple]:
        """
        搜索指定图片

        :param image_path: 要搜索的图片路径
        :param click_left: 是否左键点击找到的图片，若为 False 则使用右键点击
        :param clicks: 点击次数
        :param click_offset_x: 点击图片时的X偏移量
        :param click_offset_y: 点击图片时的Y偏移量
        :param not_click: 不点击
        :param grayscale: 是否将图片转换为灰度，大约可提升30%搜索速度，但是也可能因此造成匹配错误
        :param confidence: 图像匹配的相似度，默认为0.7
        :param auto_adjust_to_min_confidence: 是否在超时后自动降低相似度，最低相似度，每次降低0.1，默认为0.5
        :param fail_out: 超时后终止程序，默认为False
        :param timeout: 等待图片出现的超时时间（秒），默认为None：只搜索一次
        :param wait_forever: 是否一直等待，直到找到图片，默认为False
        """
        # 判断图片是否存在
        if not os.path.exists(image_path):
            log.error(f'图片 {image_path} 不存在！')
            show_custom_info("图片不存在", f"图片 {image_path} 不存在！\n 程序将退出。", display_time=5000,
                             use_thread=False)
            # 退出程序
            self.finish()

        log.info(f'搜索 {image_path}...')
        self.show_subtitle(f'搜索 {get_file_name_and_extension(image_path)[0]}...')

        start_time = time.time()
        current_confidence = confidence
        n = 1

        while True:
            location = self.get_image_center_pos(image_path, grayscale=grayscale, confidence=current_confidence,
                                                 **kwargs)
            if location:
                if not_click:
                    return location

                if click_left:
                    log.info(f'找到 {image_path} 的位置：{location}，点击左键 {clicks} 次...')
                    self.show_subtitle(
                        f'找到 {get_file_name_and_extension(image_path)[0]} 的位置：{location}，点击左键 {clicks} 次...')

                    pyautogui.click(location[0] + click_offset_x, location[1] + click_offset_y, button='LEFT',
                                    clicks=clicks)
                else:
                    log.info(f'找到 {image_path} 的位置：{location}，点击右键 {clicks} 次...')
                    self.show_subtitle(
                        f'找到 {get_file_name_and_extension(image_path)[0]} 的位置：{location}，点击右键 {clicks} 次...')
                    pyautogui.click(location[0] + click_offset_x, location[1] + click_offset_y, button='RIGHT',
                                    clicks=clicks)
                return location

            if timeout and time.time() - start_time < timeout:
                log.debug(f'等待 {image_path} 出现...')
                time.sleep(0.5)
                continue

            if wait_forever:
                time.sleep(0.5)
                current_confidence = confidence  # 重置
                if start_time + 30 * n < time.time():  # 每30秒显示一次提示信息
                    n += 1
                    show_custom_info(f"未找到 {image_path}，\n退出请按 Esc 键。", "未找到图片")
                continue

            if auto_adjust_to_min_confidence and current_confidence >= auto_adjust_to_min_confidence:
                # 降低相似度，保留0.1
                current_confidence = float(f'{current_confidence - 0.1:.1f}')
                log.info(f'未找到 {image_path}，降低相似度到 {current_confidence}...')
                self.show_subtitle(
                    f'未找到 {get_file_name_and_extension(image_path)[0]}，降低相似度到 {current_confidence}...')
                continue

            if fail_out:
                show_custom_info("无法定位图片", f"没有找到 {image_path}！\n程序将退出。", display_time=5000,
                                 use_thread=False)
                # 退出程序
                self.finish()

            log.warning(f'未找到：{image_path}')
            return None

    def wait_for_image_to_appear(self, image_path: str, confidence: float = 0.7, grayscale: bool = False,
                                 auto_adjust_to_min_confidence: float = None, fail_out: bool = False,
                                 timeout: int = 10, wait_forever: bool = False,
                                 **kwargs) -> Optional[tuple]:
        """
        等待图片出现

        :param image_path: 要等待出现的图片路径
        :param confidence: 图像匹配的相似度，这里需要自己手动测试一下，选择一个合适的值，默认为0.7
        :param grayscale: 是否将图片转换为灰度，大约可提升30%搜索速度，但是也可能因此造成匹配错误
        :param auto_adjust_to_min_confidence: 是否在超时后自动降低相似度，最低相似度，每次降低0.1，默认为0.5
        :param fail_out: 超时后终止程序，默认为False
        :param timeout: 等待图片出现的超时时间（秒）
        :param wait_forever: 是否一直等待，直到找到图片，默认为False
        """
        # 判断图片是否存在
        if not os.path.exists(image_path):
            log.error(f'图片 {image_path} 不存在！')
            show_custom_info("图片不存在", f"图片 {image_path} 不存在！\n 程序将退出。", display_time=5000,
                             use_thread=False)
            # 退出程序
            self.finish()

        log.info(f'等待图片出现：{image_path}')
        self.show_subtitle(f'等待图片出现：{get_file_name_and_extension(image_path)[0]}')

        start_time = time.time()
        current_confidence = confidence
        n = 1
        while True:
            location = self.get_image_center_pos(image_path, grayscale=grayscale, confidence=confidence, **kwargs)
            if location:
                log.info(f'找到图片：{image_path} 位置：{location}')
                self.show_subtitle(f'找到图片：{get_file_name_and_extension(image_path)[0]} 位置：{location}')
                return location

            if time.time() - start_time < timeout:
                log.debug(f'等待 {image_path} 出现...')
                time.sleep(0.5)
                continue

            if auto_adjust_to_min_confidence and current_confidence >= auto_adjust_to_min_confidence:
                # 降低相似度，保留0.1
                current_confidence = float(f'{current_confidence - 0.1:.1f}')
                log.info(f'未找到 {image_path}，降低相似度到 {current_confidence}...')
                self.show_subtitle(
                    f'未找到 {get_file_name_and_extension(image_path)[0]}，降低相似度到 {current_confidence}...')
                continue

            if wait_forever:
                time.sleep(0.5)
                current_confidence = confidence  # 重置
                if start_time + 30 * n < time.time():  # 每30秒提醒一次
                    n += 1
                    show_custom_info(f"没有等到 {image_path} 出现，\n退出请按 Esc 键。", "图片未出现")
                continue

            if fail_out:
                show_custom_info("图片未出现", f"没有等到 {image_path} 出现！\n程序将退出。", display_time=5000,
                                 use_thread=False)
                # 退出程序
                self.finish()

            log.warning(f'未等到 {image_path} 出现！')
            return None

    def wait_for_image_to_disappear(self, image_path: str, confidence: float = 0.6, grayscale: bool = False,
                                    fail_out: bool = False, timeout: int = 10, wait_forever: bool = False,
                                    **kwargs) -> Optional[bool]:
        """
        等待图片消失

        :param image_path: 要等待消失的图片路径
        :param confidence: 图像匹配的相似度，这里需要自己手动测试一下，选择一个合适的值，默认为0.7
        :param grayscale: 是否将图片转换为灰度，大约可提升30%搜索速度，但是也可能因此造成匹配错误
        :param fail_out: 超时后终止程序，默认为False
        :param timeout: 等待图片消失的超时时间（秒）
        :param wait_forever: 是否一直等待，直到消失，默认为False
        """
        # 判断图片是否存在
        if not os.path.exists(image_path):
            log.error(f'图片 {image_path} 不存在！')
            show_custom_info("图片不存在", f"图片 {image_path} 不存在！\n 程序将退出。", display_time=5000,
                             use_thread=False)
            # 退出程序
            self.finish()

        log.info(f'等待图片消失：{image_path}')
        self.show_subtitle(f'等待图片消失：{get_file_name_and_extension(image_path)[0]}')

        start_time = time.time()
        n = 1

        while True:
            if not self.get_image_center_pos(image_path, grayscale=grayscale, confidence=confidence, **kwargs):
                # 再次判断，防止误判
                if not self.get_image_center_pos(image_path, grayscale=grayscale, confidence=confidence, **kwargs):
                    log.info(f'图片已消失：{image_path}')
                    self.show_subtitle(f'图片已消失：{get_file_name_and_extension(image_path)[0]}')
                    return True

            if time.time() - start_time < timeout:
                log.debug(f'等待 {image_path} 消失...')
                time.sleep(0.5)
                continue

            if wait_forever:
                time.sleep(0.5)
                if start_time + 30 * n < time.time():  # 每30秒提醒一次
                    n += 1
                    show_custom_info(f"没有等到 {image_path} 消失，\n退出请按 Esc 键。", "图片未消失")
                continue

            if fail_out:
                show_custom_info("图片未消失", f"没有等到 {image_path} 消失！\n程序将退出。", display_time=5000,
                                 use_thread=False)
                # 退出程序
                self.finish()

            log.warning(f'未等到 {image_path} 消失！')
            return False

    def get_url_title(self, url: str) -> Optional[str]:
        """
        获取指定URL的网页标题

        :param url: 要获取标题的网页URL
        :return: 网页标题，如果无法获取则返回None
        """
        try:
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
            }
            # 使用 httpx 获取网页内容
            response = httpx.get(url, headers=headers)
            response.raise_for_status()  # 检查请求是否成功

            # 使用 parsel 解析 HTML
            selector = Selector(text=response.text)
            title = selector.xpath('//title/text()').get()
            if not title:
                self.show_subtitle("无法获取标题...")
                return None

            return title.strip()
        except httpx.RequestError as e:
            log.debug(f"请求错误: {e}")
            return None
        except Exception as e:
            log.debug(f"解析错误: {e}")
            return None

    @staticmethod
    def paste_text(text: str):
        """
        将文字放入粘贴板并粘贴。

        :param text: 需要粘贴的文字
        """
        log.info(f'粘贴文本：{text}')
        pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'v')

    def finish(self):
        """结束程序"""
        log.info('程序结束，取消窗口置顶，键盘监听...')
        # 取消置顶
        self.cancel_topmost()
        # 取消监听
        if self.start_safe_mode:
            # 停止监听
            self.listener.stop_all_listening()

    def __del__(self):
        self.finish()
