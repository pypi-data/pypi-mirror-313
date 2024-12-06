# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/27 6:12
# 文件名称： image_utils.py
# 项目描述： 图片处理工具
# 开发工具： PyCharm
import os
import base64
from typing import Optional, List
from xiaoqiangclub.config.log_config import log


def image_to_base64(
        image_path_or_folder: str,
        output_file: Optional[str] = None,
        save_dir: Optional[str] = None,
        image_extensions: Optional[List[str]] = None
) -> Optional[dict]:
    """
    将指定的图片文件或包含图片的文件夹中的所有图片转换为 base64 编码，并将其保存在一个类中。

    :param image_path_or_folder: 包含图片的文件夹路径或单个图片文件路径。
    :param output_file: 输出的 Python 文件名。如果为 None，则根据文件夹名生成。
    :param save_dir: 输出文件保存的目录。默认是与 image_path_or_folder 同目录。
    :param image_extensions: 要转换的图片后缀列表。默认支持['.png', '.jpg', '.jpeg', '.gif', '.bmp']。
    :return: 一个包含所有图片的 Python 字典，键为文件名，值为 base64 编码的字符串。
    """
    if not os.path.exists(image_path_or_folder):
        raise FileNotFoundError(f"指定的路径不存在: {image_path_or_folder}")

    if output_file is None:
        base_name = os.path.basename(image_path_or_folder.rstrip('/').rstrip('\\'))
        output_file = f"{base_name}_images.py" if os.path.isdir(
            image_path_or_folder) else f"{base_name.split('.')[0]}_images.py"

    # 将 save_dir 默认设置为与 image_path_or_folder 相同的目录
    save_dir = save_dir or os.path.dirname(image_path_or_folder)
    output_path = os.path.join(save_dir, output_file)

    if image_extensions is None:
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']

    image_extensions_set = set(image_extensions)
    base64_images = {}
    file_names = []  # 用于汇总所有文件名

    try:
        if os.path.isdir(image_path_or_folder):
            for filename in os.listdir(image_path_or_folder):
                if any(filename.lower().endswith(ext) for ext in image_extensions_set):
                    file_path = os.path.join(image_path_or_folder, filename)
                    try:
                        with open(file_path, 'rb') as image_file:
                            base64_encoded = base64.b64encode(image_file.read()).decode('utf-8')
                            property_name = filename.split('.')[0] + '_' + filename.split('.')[-1]
                            base64_images[property_name] = base64_encoded
                            file_names.append(filename)  # 添加文件名到列表
                    except Exception as e:
                        log.error(f"无法读取文件 {file_path}: {e}")
        elif os.path.isfile(image_path_or_folder):
            filename = os.path.basename(image_path_or_folder)
            if any(filename.lower().endswith(ext) for ext in image_extensions_set):
                try:
                    with open(image_path_or_folder, 'rb') as image_file:
                        base64_encoded = base64.b64encode(image_file.read()).decode('utf-8')
                        property_name = filename.split('.')[0] + '_' + filename.split('.')[-1]
                        base64_images[property_name] = base64_encoded
                        file_names.append(filename)  # 添加文件名到列表
                except Exception as e:
                    log.error(f"无法读取文件 {image_path_or_folder}: {e}")
        else:
            log.warning(f"指定的路径不是文件或文件夹: {image_path_or_folder}")

        # 将 Base64 编码的图片写入 Python 文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# 自动生成的文件，包含 base64 编码的图片\n")
            f.write("image_files = [\n")  # 开始生成文件名列表
            for name in file_names:
                f.write(f"    '{name}',\n")  # 写入文件名
            f.write("]\n")  # 结束文件名列表
            f.write("class Base64Images:\n")
            for property_name, encoded in base64_images.items():
                f.write(f"    {property_name} = '{encoded}'\n")

        log.info(f"Base64 编码的图片已保存到 {output_path}")

    except Exception as e:
        log.error(f"{image_path_or_folder} 转换为Base64发生错误: {e}")

    return base64_images
