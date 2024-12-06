# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/21 07:13
# 文件名称： image_utils.py
# 项目描述： 图片处理工具
# 开发工具： PyCharm
import os
import win32ui
import win32gui
from typing import Optional
from PIL import (Image, ImageFilter)
from xiaoqiangclub.config.log_config import log


def get_file_icon(file_path: str, output_path: str = None, size: int = 256) -> Optional[str]:
    """
    提取文件的图标并保存为背景透明的图片，同时增强边缘的平滑度

    :param file_path: str 文件的路径
    :param output_path: str 图标图片保存的路径，如果为 None，则默认保存在文件所在目录。
    :param size: int 图片的尺寸（正方形边长），默认值为256
    :return: Optional[str] 保存的图片路径，如果失败返回 None
    """
    try:
        large, small = win32gui.ExtractIconEx(file_path, 0)
        if not large:
            log.error("未能提取到图标")
            return None
        win32gui.DestroyIcon(small[0])

        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, 32, 32)
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)
        hdc.DrawIcon((0, 0), large[0])

        bmpinfo = hbmp.GetInfo()
        bmpstr = hbmp.GetBitmapBits(True)
        icon = Image.frombuffer('RGBA', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRA', 0, 1)

        # 转换为RGBA并设置透明度
        icon = icon.convert("RGBA")
        datas = icon.getdata()

        new_data = []
        for item in datas:
            if item[:3] == (0, 0, 0):
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)

        icon.putdata(new_data)

        # 将图标按指定尺寸缩放，并创建一个新的透明图像
        original_size = icon.size
        scale = min(size / original_size[0], size / original_size[1])
        new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
        icon = icon.resize(new_size, Image.Resampling.LANCZOS)

        # 使用LANCZOS算法提高边缘平滑度
        result_icon = Image.new("RGBA", (size, size), (255, 255, 255, 0))
        position = ((size - new_size[0]) // 2, (size - new_size[1]) // 2)

        result_icon.paste(icon, position, icon)

        # 增加边缘平滑处理,使用抗锯齿效果的平滑滤镜
        result_icon = result_icon.filter(ImageFilter.SMOOTH_MORE)

        # 获取原文件的名称
        file_name, _ = os.path.splitext(os.path.basename(file_path))

        if not output_path:  # 如果没有提供保存路径，默认保存到原图片目录
            output_path = os.path.join(os.path.dirname(file_path), f"{file_name}_icon.png")

        result_icon.save(output_path, "PNG")
        win32gui.DestroyIcon(large[0])
        log.info(f"图标提取到： {output_path}")
        return output_path

    except Exception as e:
        log.error(f"提取图标失败: {e}")
        return None
