# _*_ coding : UTF-8 _*_
# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/23 7:16
# 文件名称： zip.py
# 项目描述： 压缩文件管理工具
# 开发工具： PyCharm
import os
import shutil
import pyzipper
from typing import Optional, Union, List
from xiaoqiangclub.config.log_config import log


def rename_file(original_path: str, new_name: str) -> None:
    """重命名文件或文件夹。

    :param original_path: 要重命名的文件或文件夹的原始路径。
    :param new_name: 新的名称（不包含路径）。
    """
    directory = os.path.dirname(original_path)  # 获取文件的目录
    new_path = os.path.join(directory, new_name)  # 构造新的文件路径
    try:
        os.rename(original_path, new_path)  # 重命名文件或文件夹
        log.info(f"重命名成功: {original_path} -> {new_path}")  # 记录重命名成功的日志
    except Exception as e:
        log.error(f"重命名失败: {e}")  # 记录重命名失败的日志


def add_files_to_zip(zip_file_path: str, files_to_add: List[Union[str, bytes]], password: Optional[str] = None,
                     delete_source: bool = False, new_names: Optional[List[str]] = None,
                     new_zip_file_path: Optional[str] = None) -> Optional[str]:
    """将文件或文件夹添加到 ZIP 文件中并可选设置密码。

    :param zip_file_path: 目标 ZIP 文件的路径。
    :param files_to_add: 要添加的文件或文件夹路径列表。
    :param password: 可选的密码，用于加密 ZIP 文件。
    :param delete_source: 是否删除源文件，默认为 False。
    :param new_names: 可选的新文件名列表，对应 files_to_add，如果提供，将使用这些新名称替换文件名称。
    :param new_zip_file_path: 新的 ZIP 文件路径，如果提供，将生成一个新的 ZIP 文件而不修改原始 new_zip_file_path 文件。
    """
    try:
        if not new_zip_file_path:
            new_zip_file_path = zip_file_path
        else:
            # 确保新文件路径以 .zip 结尾
            new_zip_file_path = new_zip_file_path.split('.')[0] + '.zip'
            new_zip_file_path = os.path.abspath(new_zip_file_path)

            # 复制原始 zip 文件到新路径
            shutil.copy2(zip_file_path, new_zip_file_path)
            log.info(f"已复制 ZIP 文件到新路径: {new_zip_file_path}")

        with pyzipper.AESZipFile(new_zip_file_path, 'a', compression=pyzipper.ZIP_DEFLATED,
                                 encryption=pyzipper.WZ_AES if password else None) as zip_file:
            if password:
                zip_file.setpassword(password.encode('utf-8'))  # 设置密码

            for i, file_to_add in enumerate(files_to_add):
                if os.path.isfile(file_to_add):  # 如果是文件
                    arcname = new_names[i] if new_names and len(new_names) > i else os.path.basename(file_to_add)
                    zip_file.write(file_to_add, arcname)  # 添加文件
                    log.info(f"已添加: {file_to_add}")  # 记录添加文件的信息
                elif os.path.isdir(file_to_add):  # 如果是文件夹
                    for root, _, files in os.walk(file_to_add):  # 遍历文件夹
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, start=os.path.dirname(file_to_add))
                            zip_file.write(file_path, arcname)  # 添加文件
                            log.info(f"已添加: {file_path}")  # 记录添加文件的信息
                else:
                    log.warning(f"{file_to_add} 不是有效的文件或文件夹。")  # 记录警告

        log.info(f"压缩完成！目标 ZIP 文件路径：{new_zip_file_path}")

        if delete_source:  # 如果需要删除源文件
            for file_to_add in files_to_add:
                if os.path.isfile(file_to_add):
                    os.remove(file_to_add)  # 删除文件
                    log.info(f"源文件已删除: {file_to_add}")  # 记录删除文件的信息
                elif os.path.isdir(file_to_add):
                    shutil.rmtree(file_to_add)  # 删除文件夹
                    log.info(f"源文件夹已删除: {file_to_add}")  # 记录删除文件夹的信息

        return new_zip_file_path  # 返回生成的 ZIP 文件的绝对路径
    except FileNotFoundError:
        log.error("文件或 ZIP 文件不存在。")  # 记录错误
    except Exception as e:
        log.error(f"发生错误: {e}")  # 记录错误


def zip_file(files: List[Union[str, bytes]], new_zip_file_path: str, password: Optional[str] = None,
             delete_source: bool = False) -> Optional[str]:
    """
    压缩指定的文件和文件夹到 ZIP 文件中，并可设置密码。

    :param files: 要压缩的文件和文件夹路径列表。
    :param new_zip_file_path: 目标 ZIP 文件的路径。
    :param password: 可选的密码，用于加密 ZIP 文件。
    :param delete_source: 可选的参数，设置为 True 会在压缩完成后删除源文件或文件夹。
    """
    try:
        with pyzipper.AESZipFile(new_zip_file_path, 'w', compression=pyzipper.ZIP_DEFLATED,
                                 encryption=pyzipper.WZ_AES if password else None) as zip_file:
            if password:
                zip_file.setpassword(password.encode('utf-8'))  # 设置密码

            for item in files:
                if os.path.isfile(item):  # 如果是文件
                    zip_file.write(item, os.path.basename(item))  # 添加文件
                    if delete_source:  # 如果需要删除源文件
                        os.remove(item)  # 删除文件
                        log.info(f"已删除文件: {item}")

                elif os.path.isdir(item):  # 如果是文件夹
                    for root, _, files_in_dir in os.walk(item):  # 遍历文件夹
                        for file in files_in_dir:
                            file_path = os.path.join(root, file)
                            # 使用相对路径保持文件夹结构
                            arcname = os.path.relpath(file_path, start=os.path.dirname(item))
                            zip_file.write(file_path, arcname)  # 添加文件
                    if delete_source:  # 如果需要删除文件夹
                        os.rmdir(item)  # 删除文件夹
                        log.info(f"已删除文件夹: {item}")

                else:
                    log.warning(f"{item} 不是有效的文件或文件夹。")  # 记录警告

        log.info(f"压缩成功！压缩文件路径：{new_zip_file_path}")  # 记录压缩成功的信息
        return new_zip_file_path

    except FileNotFoundError:
        log.error("文件或文件夹不存在。")  # 记录错误
    except Exception as e:
        log.error(f"发生错误: {e}")  # 记录错误


def decode_filename(encoded_name: str) -> str:
    """
    解码 ZIP 文件中的文件名，解决中文乱码问题。

    :param encoded_name: 已编码的文件名
    :return:
    """
    try:
        # 尝试使用 utf-8 解码
        return encoded_name.encode('cp437').decode('utf-8')
    except (UnicodeDecodeError, AttributeError):
        try:
            # 如果 utf-8 解码失败，尝试使用 gbk 解码
            return encoded_name.encode('cp437').decode('gbk')
        except UnicodeDecodeError:
            return encoded_name  # 返回原始名称，若解码失败
    except Exception as e:
        log.debug(f"解码文件名时发生错误: {e}")
        return encoded_name  # 返回原始名称，若解码失败


def unzip_file(zip_file_path: str, target_folder: str, password: Optional[str] = None) -> None:
    """
    解压 ZIP 文件到指定文件夹。

    :param zip_file_path: ZIP 文件的路径。
    :param target_folder: 目标文件夹的路径。
    :param password: 可选的密码，用于解压 ZIP 文件。
    :return:
    """
    try:
        with pyzipper.AESZipFile(zip_file_path, 'r') as zip_file:
            if password:
                zip_file.setpassword(password.encode('utf-8'))  # 设置密码
            for info in zip_file.infolist():
                file_name = decode_filename(info.filename)  # 使用解码函数处理文件名
                file_path = os.path.join(target_folder, file_name)
                if info.is_dir():
                    os.makedirs(file_path, exist_ok=True)
                else:
                    with zip_file.open(info) as source:
                        # 确保在写入时不引发编码错误
                        with open(file_path, 'wb') as target:
                            target.write(source.read())
            log.info(f"解压完成！解压到：{target_folder}")
    except FileNotFoundError:
        log.error("ZIP 文件不存在。")  # 记录错误
    except pyzipper.BadZipFile:
        log.error("ZIP 文件损坏。")  # 记录错误
    except RuntimeError as e:
        log.error(f"密码错误或解压失败: {e}")  # 记录错误
    except Exception as e:
        log.error(f"发生错误: {e}")  # 记录错误


def remove_zip_password(zip_file_path: str, password: str) -> None:
    """
    移除 ZIP 文件的密码
    注意： 这里存在一个bug，含有中文的文件名称会乱码。

    :param zip_file_path: zip压缩文件路径
    :param password: 压缩密码
    """
    try:
        temp_zip_file_path = zip_file_path.replace('.zip', '_temp.zip')
        with pyzipper.AESZipFile(zip_file_path) as original_zip:
            original_zip.setpassword(password.encode('utf-8'))  # 设置提供的密码
            with pyzipper.AESZipFile(temp_zip_file_path, 'w', compression=pyzipper.ZIP_DEFLATED) as new_zip:
                for file_info in original_zip.infolist():
                    # 处理文件名解码
                    file_name = decode_filename(file_info.filename)
                    new_zip.writestr(file_name, original_zip.read(file_info.filename))
        os.replace(temp_zip_file_path, zip_file_path)  # 替换原 ZIP 文件
        log.info("密码移除成功。")
    except FileNotFoundError:
        log.error("ZIP 文件不存在。")
    except RuntimeError:
        log.error("提供的密码错误，无法移除密码。")  # 记录密码错误
    except Exception as e:
        log.error(f"发生错误: {e}")


def change_zip_password(zip_file_path: str, old_password: str, new_password: str) -> None:
    """
    修改 ZIP 文件的密码
    注意： 这里存在一个bug，含有中文的文件名称会乱码。

    :param zip_file_path: 要修改密码的 ZIP 文件路径。
    :param old_password: 原密码。
    :param new_password: 新密码。
    """
    try:
        temp_zip_file_path = zip_file_path.replace('.zip', '_temp.zip')  # 创建临时 ZIP 文件路径
        with pyzipper.AESZipFile(zip_file_path) as original_zip:
            original_zip.setpassword(old_password.encode('utf-8'))  # 设置原密码
            with pyzipper.AESZipFile(temp_zip_file_path, 'w', compression=pyzipper.ZIP_DEFLATED,
                                     encryption=pyzipper.WZ_AES) as new_zip:
                for file_info in original_zip.infolist():
                    file_name = decode_filename(file_info.filename)
                    new_zip.setpassword(new_password.encode('utf-8'))  # 设置新密码
                    new_zip.writestr(file_name, original_zip.read(file_info.filename))  # 复制文件内容
        os.replace(temp_zip_file_path, zip_file_path)  # 替换原 ZIP 文件
        log.info(f"密码已修改为：{new_password}")  # 记录成功信息
    except FileNotFoundError:
        log.error("ZIP 文件不存在。")  # 记录错误
    except RuntimeError:
        log.error("原密码错误，无法修改密码。")  # 记录错误
    except Exception as e:
        log.error(f"发生错误: {e}")  # 记录错误


def set_zip_password(zip_file_path: str, password: str) -> None:
    """
    为现有 ZIP 文件添加密码
    注意： 这里存在一个bug，含有中文的文件名称会乱码。

    :param zip_file_path: 要添加密码的 ZIP 文件路径。
    :param password: 要设置的新密码。
    """
    try:
        temp_zip_file_path = zip_file_path.replace('.zip', '_temp.zip')  # 创建临时 ZIP 文件路径
        with pyzipper.AESZipFile(zip_file_path) as original_zip:
            with pyzipper.AESZipFile(temp_zip_file_path, 'w', compression=pyzipper.ZIP_DEFLATED,
                                     encryption=pyzipper.WZ_AES) as new_zip:
                new_zip.setpassword(password.encode('utf-8'))  # 设置新密码
                for file_info in original_zip.infolist():
                    file_name = decode_filename(file_info.filename)
                    new_zip.writestr(file_name, original_zip.read(file_info.filename))  # 复制文件内容
        os.replace(temp_zip_file_path, zip_file_path)  # 替换原 ZIP 文件
        log.info(f"已添加密码：{password}")  # 记录成功信息
    except FileNotFoundError:
        log.error("ZIP 文件不存在。")  # 记录错误
    except Exception as e:
        log.error(f"发生错误: {e}")  # 记录错误


def crack_zip_password(zip_file_path: str, password_list: List[str]) -> Optional[str]:
    """
    破解 ZIP 文件密码。

    :param zip_file_path: ZIP 文件路径，字符串类型。
    :param password_list: 密码列表，字符串类型列表。
    :return: 如果找到密码，返回密码；否则返回 None。
    """
    try:
        with pyzipper.AESZipFile(zip_file_path) as zip_file:
            for password in password_list:  # 遍历密码列表
                try:
                    zip_file.setpassword(password.encode('utf-8'))  # 设置当前密码
                    # 尝试访问文件列表而不解压
                    zip_file.testzip()  # 测试密码有效性
                    log.info(f"破解成功，密码: {password}")  # 记录成功信息
                    return password  # 找到密码，返回
                except RuntimeError:
                    continue  # 密码不正确，继续尝试下一个
            log.warning("未能找到正确的密码。")  # 记录未找到密码的警告
            return None  # 未找到密码
    except FileNotFoundError:
        log.error("ZIP 文件不存在。")  # 记录错误
    except Exception as e:
        log.error(f"发生错误: {e}")  # 记录错误
