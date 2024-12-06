# _*_ coding : UTF-8 _*_
# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/03 12:50
# 文件名称： encrypt_utils.py
# 项目描述： 简单的加解密实现
# 开发工具： PyCharm
import os
import base64
from typing import Optional
from xiaoqiangclub.config.log_config import log


class SimpleCrypto:
    """
    简单的加解密实现
    """

    @staticmethod
    def generate_key(save_to_file: Optional[str] = None) -> str:
        """
        生成一个随机密钥，并可选择保存到文件

        :param save_to_file: 可选，指定保存密钥的文件路径
        :return: 返回 Base64 编码的随机密钥
        """
        try:
            key = os.urandom(16)  # 生成 16 字节的随机密钥
            encoded_key = base64.urlsafe_b64encode(key).decode('utf-8')

            if save_to_file:
                with open(save_to_file, 'w', encoding='utf-8') as f:
                    f.write(encoded_key)
                log.info(f"密钥已保存到 {save_to_file}")

            log.info(f"生成的密钥: {encoded_key}")
            return encoded_key
        except Exception as e:
            log.error(f"生成密钥时出错: {e}")
            raise

    @staticmethod
    def encrypt(data: str, key: Optional[str] = None, save_to_file: Optional[str] = None) -> str:
        """
        加密数据，并可选择保存加密结果到文件

        :param data: 需要加密的数据，必须是字符串
        :param key: 加密密钥，必须是 Base64 编码的字符串；如果为 None，则自动生成密钥并保存
        :param save_to_file: 可选，指定保存加密数据的文件路径
        :return: 加密后的数据，返回字符串
        """
        try:
            if key is None:
                key = SimpleCrypto.generate_key(save_to_file='generated_key.txt')  # 自动生成并保存密钥

            key_bytes = base64.urlsafe_b64decode(key)
            data_bytes = data.encode('utf-8')
            encrypted_bytes = bytes([data_bytes[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data_bytes))])
            encrypted_data = base64.urlsafe_b64encode(encrypted_bytes).decode('utf-8')

            if save_to_file:
                with open(save_to_file, 'w', encoding='utf-8') as f:
                    f.write(f"原始数据: {data}\n")
                    f.write(f"加密密钥: {key}\n")
                    f.write(f"加密数据: {encrypted_data}\n")
                log.info(f"加密数据已保存到 {save_to_file}")

            return encrypted_data
        except Exception as e:
            log.error(f"加密数据时出错: {e}")
            raise

    @staticmethod
    def decrypt(encrypted_data: str, key: str) -> str:
        """
        解密数据

        :param encrypted_data: 需要解密的数据，必须是字符串
        :param key: 解密密钥，必须是 Base64 编码的字符串
        :return: 解密后的数据，返回字符串
        """
        try:
            key_bytes = base64.urlsafe_b64decode(key)
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data)
            decrypted_bytes = bytes(
                [encrypted_bytes[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(encrypted_bytes))])
            return decrypted_bytes.decode('utf-8')
        except Exception as e:
            log.error(f"解密数据时出错: {e}")
            raise
