# _*_ coding : UTF-8 _*_
# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/23 12:25
# 文件名称： prompt_tone.py
# 项目描述： 播放系统声音
# 开发工具： PyCharm
import os
import platform
import winsound
from typing import Optional
from xiaoqiangclub.config.log_config import log


def play_system_sound(sound_type: Optional[str] = 'default', custom_sound: Optional[str] = None) -> None:
    """
    播放系统自带的声音或自定义音效，支持 Windows 和 macOS。

    :param sound_type: 系统声音类型。Windows: 可选 'default', 'systemhand', 'exclamation', 'asterisk', 'question'。
                        macOS: 'default'。
    :param custom_sound: 自定义音效文件路径，如果提供则播放此音效文件。
    """
    try:
        current_os = platform.system()
        if custom_sound and os.path.isfile(custom_sound):
            if current_os == "Windows":
                winsound.PlaySound(custom_sound, winsound.SND_FILENAME)
            elif current_os == "Darwin":  # macOS
                os.system(f"afplay {custom_sound}")
            else:
                raise NotImplementedError("当前操作系统不支持播放自定义音效。")
        else:
            if current_os == "Windows":
                sounds = {
                    'default': winsound.MB_OK,
                    'systemhand': winsound.MB_ICONHAND,
                    'exclamation': winsound.MB_ICONEXCLAMATION,
                    'asterisk': winsound.MB_ICONASTERISK,
                    'question': winsound.MB_ICONQUESTION,
                }
                if sound_type in sounds:
                    winsound.MessageBeep(sounds[sound_type])
                else:
                    raise ValueError(
                        "无效的声音类型。可选类型：'default', 'exclamation', 'systemhand', 'asterisk', 'question'。")
            elif current_os == "Darwin":  # macOS
                os.system("osascript -e 'beep'")
            else:
                raise NotImplementedError("当前操作系统不支持播放系统声音。")

        log.debug(f"已播放声音: {'自定义音效' if custom_sound else sound_type}")
    except Exception as e:
        log.error(f"发生错误: {e}")
