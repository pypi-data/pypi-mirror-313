# _*_ coding : UTF-8 _*_
# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2023/8/24 13:09
# 文件名称： ctfile.py
# 项目描述： 城通网盘接口，并在原来的代码基础上打包成了伪异步函数
# 开发工具： PyCharm
# 接口说明：https://openapi.ctfile.com/docs/ctfile-open-api/ctfile-open-api-1c9jul3u611q2
import os
import asyncio
import hashlib
from xiaoqiangclub.config.log_config import log
from typing import (Optional, List, Literal, Union)
from xiaoqiangclub.data.file import (write_file_async, read_file_async)
from xiaoqiangclub.utils.network_utils import get_response_async


class Ctfile:
    def __init__(self, account: Optional[str] = None, password: Optional[str] = None, token: Optional[str] = None,
                 save_token_path: str = None):
        """
        城通网盘的接口封装，优先使用 token，若没有则使用邮箱和密码获取 token
        https://openapi.ctfile.com/docs/ctfile-open-api/ctfile-open

        :param account: 用户邮箱/手机
        :param password: 用户密码
        :param token: 访问 token
        :param save_token_path: 保存 token 的路径，当使用账号和密码登录时，会自动保存 token，下次使用 token 登录。
        """
        self.save_token_path = save_token_path or os.path.join(os.getcwd(), 'ctfile_token.txt')

        if token:
            self.token = token
        elif account and password:
            self.token = asyncio.run(self.__get_shot_time_token(account, password))
            if not self.token:
                raise ValueError("无法获取到 token，请检查账号和密码是否正确。")
        else:
            raise ValueError("请提供有效的 token 或邮箱和密码。")

    @staticmethod
    async def __get_json_data(url: str, data: dict = None) -> Optional[dict]:
        """
        发送请求，返回json数据
        :param url: 请求地址
        :param data: 请求数据
        :return:
        """
        json_data = await get_response_async(url, json=data, return_json=True)
        if json_data and json_data.get("code") != 200:
            log.error(f"获取数据失败：{json_data}")
            return None
        log.debug(f'获取到返回数据：{json_data}')
        return json_data

    async def __get_shot_time_token(self, email: str, password: str) -> Optional[str]:
        """
        通过邮箱密码获取3天有效期的临时token
        :param email: 邮箱
        :param password: 密码
        :return: 访问成功则返回临时token
        """
        # 尝试从本地读取token
        if os.path.exists(self.save_token_path):
            short_time_token = await read_file_async(self.save_token_path)
            self.token = short_time_token.strip()

        if self.token:
            # 判断token是否过期
            if await self.check_token():
                return self.token

        data = {'email': email, 'password': password}

        json_data = await self.__get_json_data(url='https://rest.ctfile.com/v1/user/auth/login', data=data)
        short_time_token = json_data.get('token')
        log.info('获取到临时token：' + short_time_token)
        await write_file_async(self.save_token_path, short_time_token)
        return short_time_token

    async def check_token(self) -> bool:
        """
        检测token是否过期
        :return:
        """
        user_info = await self.get_user_info()  # {'code': 401, 'message': '未登录'}
        if user_info.get('code') == 200:
            return True
        return False

    async def get_user_info(self) -> Optional[dict]:
        """
        获取用户信息
        :return: None
        """
        data = {'session': self.token}
        return await self.__get_json_data(url='https://rest.ctfile.com/v1/user/info/profile', data=data)

    async def get_public_folder_info(self, parent_folder_id: str = 'd0') -> Optional[List[dict]]:
        """
        获取公有云文件夹列表
        https://openapi.ctfile.com/docs/ctfile-open-api/ctfile-open-api-1c9m8uh3njlcv
        :param parent_folder_id: 父文件夹ID，根目录为d0
        :return:
        """
        data = {"folder_id": parent_folder_id, "session": self.token}
        json_data = await self.__get_json_data(url='https://rest.ctfile.com/v1/public/folder/list', data=data)
        if not json_data:
            return None
        return json_data.get('results')

    async def get_public_all_folder_info(self, folder_id: str = 'd0', folder_path: str = ''):
        """
        获取公有云所有文件夹信息
        :param folder_id: 父文件夹ID，根目录为d0
        :param folder_path: 文件夹路径
        :return:
        """
        folder_info = await self.get_public_folder_info(folder_id)
        all_folder_info = [
            {'folder_name': '根目录', 'folder_id': 'd0', 'folder_path': '/'}] if folder_id == 'd0' else []

        if folder_info:
            for folder in folder_info:
                folder_name = folder.get('name')  # 文件夹名称
                folder_id = folder.get('key')  # 文件夹ID
                # 文件夹路径
                start_folder_path = folder_path + '/' + folder_name  # 文件夹路径
                all_folder_info.append({
                    'folder_name': folder_name,
                    'folder_id': folder_id,
                    'folder_path': start_folder_path  # 文件夹路径
                })
                folder_info_list = await self.get_public_all_folder_info(folder_id, start_folder_path)
                all_folder_info.extend(folder_info_list)

        return all_folder_info

    @staticmethod
    def split_path(path: str) -> list:
        """
        将路径拆分为列表，去空
        :param path: 路径
        :return:
        """
        # 使用 os.path.normpath 规范化路径
        normalized_path = os.path.normpath(path)
        # 使用 os.path.split 逐层拆分路径
        path_list = normalized_path.split(os.sep)
        # 去除空元素
        path_list = [item for item in path_list if item]
        return path_list

    async def get_public_folder_id(self, folder_path: str) -> Optional[str]:
        """
        获取公有云文件夹ID
        :param folder_path: 文件夹路径，例如
        :return:
        """
        all_folder_info = await self.get_public_all_folder_info()
        for folder in all_folder_info:
            path = folder.get('folder_path')
            if self.split_path(path) == self.split_path(folder_path):
                return folder.get('folder_id')

        return None

    async def search_file(self, keyword: str) -> Optional[list]:
        """
        搜索文件
        :param keyword: 关键词
        :return:
        """
        json_data = await self.get_public_folder_files(folder_id='d0', keyword=keyword)
        if not json_data:
            log.error(f'搜索 关键词 {keyword} 失败！')
            return None
        return json_data

    async def get_public_folder_files(self, folder_path: str = None, folder_id: str = None, start: str = '0',
                                      reload: Literal[0, 1] = 0,
                                      order_by: Literal['old', 'az', 'za', 'big', 'small', 'new'] = None,
                                      filter: Literal[
                                          'video', 'music', 'picture', 'document', 'app', 'zip', 'other'] = None,
                                      keyword: str = None) -> Optional[list]:
        """
        获取公有云指定文件夹下的所有文件信息
        https://openapi.ctfile.com/docs/ctfile-open-api/ctfile-open-api-1c9kitkmo2gm8

        :param folder_path: 文件夹路径
        :param folder_id: 文件夹ID
        :param start: 起始位置，默认每次获取50条数据
        :param order_by: 文件排序:old,az,za,big,small,new。new,old新旧排序，az,za，A-Z/Z-A排序，big,small，从文件大到小，小到大排序， 共6个排序方式
        :param reload: 1 为获取0至start位置的所有数据，默认为0，从start获取50条数据
        :param filter: 文件类型，可选值：video,music,picture,document,app,zip,other。默认为空，即全部文件类型
        :param keyword: 列举包含关键字的文件和文件夹
        :return: 公有云文件列表
        """
        # 获取文件夹id
        folder_id = folder_id or await self.get_public_folder_id(folder_path)

        if not folder_id:
            log.error(f'没有找到公有云目录：{folder_path}...')
            return None

        data = {
            "session": self.token,
            "folder_id": folder_id,
            "start": start,
            "orderby": order_by,
            "filter": filter,
            'reload': reload,
            'keyword': keyword
        }

        json_data = await self.__get_json_data(url='https://rest.ctfile.com/v1/public/file/list', data=data)
        if not json_data:
            log.error(f'获取公有云 {folder_path} 的文件列表失败！')
            return None

        return json_data.get('results')

    async def get_public_all_files(self):
        """
        获取公有云所有文件信息
        :return:
        """
        all_folder_info = await self.get_public_all_folder_info()
        if not all_folder_info:
            log.error('获取公有云所有文件数信息失败！')

        # 获取所有文件夹id:['d0', 'd63670780', 'd63670783', 'd30252727', 'd48553877']
        folder_ids = [folder.get('folder_id') for folder in all_folder_info]

        # 创建并发任务
        all_files = await asyncio.gather(*[self.get_public_folder_files(folder_id=id) for id in folder_ids])

        # 展开到一个列表
        all_files = [item for sublist in all_files if sublist for item in sublist]

        return all_files

    async def get_share_link(self, file_name: Union[str, List[str]] = None,
                             file_ids: Union[str, List[str]] = None) -> Optional[list]:
        """
        获取分享链接
        :param file_name: 文件名，支持多个文件名，例如 ['1.txt','2.txt']
        :param file_ids: 文件id，支持多个文件id，例如 ['d0_1','d0_2']
        :return: 分享链接详情列表
        """
        if isinstance(file_name, str):
            file_name = [file_name]

        if file_name:
            # 创建并发搜索
            search_result_list = await asyncio.gather(*[self.search_file(name) for name in file_name])
            # 获取相关文件/文件夹id
            file_ids = [item.get('key') for sublist in search_result_list for item in sublist]

        if not file_ids:
            log.error(f'没有找到公有云文件：{file_name}...')
            return None

        data = {"session": self.token, "ids": file_ids}
        json_data = await self.__get_json_data('https://rest.ctfile.com/v1/public/file/share', data)

        if not json_data:
            log.error(f'获取 {file_name} 的分享链接失败！')
            return None

        return json_data.get('results')

    async def get_public_all_share_links(self) -> List[dict]:
        """
        获取公有云所有文件分享链接
        :return:
        """
        log.info('开始获取城通网盘公有云所有文件分享链接，请耐心等待...')
        all_files = await self.get_public_all_files()
        all_ids = [file.get('key') for file in all_files]
        return await self.get_share_link(file_ids=all_ids)

    @staticmethod
    def calculate_checksum(file_path: str) -> str:
        """
        计算文件的 SHA1 校验和
        :param file_path: 文件路径
        :return: SHA1 校验和
        """
        sha1 = hashlib.sha1()
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(65536)  # 每次读取64K
                if not data:
                    break
                sha1.update(data)
        return sha1.hexdigest()

    async def get_upload_url(self, folder_id: str, checksum: str, size: int, name: str) -> Optional[str]:
        """
        获取文件上传的 URL
        https://openapi.ctfile.com/docs/ctfile-open-api/ctfile-open-api-1c9m4d9fhfs5j
        :param folder_id: 目录id
        :param checksum: 文件的 checksum
        :param size: 文件大小
        :param name: 文件名
        :return: 上传url
        """
        url = 'https://rest.ctfile.com/v1/public/file/upload'
        data = {
            "session": self.token,
            "folder_id": folder_id,
            "checksum": checksum,
            "size": size,
            "name": name
        }
        try:
            json_data = await self.__get_json_data(url, data)
            upload_url = json_data.get('upload_url')
            log.debug('获取到上传url：' + upload_url)
            return upload_url
        except Exception as e:
            log.error('获取上传URL失败：' + str(e))
            return None

    async def upload_file(self, upload_file_path: str, save_path: str) -> Optional[str]:
        """
        上传文件到指定目录
        :param upload_file_path: 文件路径
        :param save_path: 保存到公有云盘的路径
        :return: 上传结果（文件id）
        """
        if not os.path.exists(upload_file_path):
            log.error(f'文件不存在：{upload_file_path}')
            return None

        # 获取文件夹id
        folder_id = await self.get_public_folder_id(save_path)
        if not folder_id:
            log.error(f'没有找到公有云目录：{save_path}，请先创建....')
            return None

        file_size = os.path.getsize(upload_file_path)
        file_name = os.path.basename(upload_file_path)
        checksum = self.calculate_checksum(upload_file_path)

        upload_url = await self.get_upload_url(folder_id, checksum, file_size, file_name)
        if not upload_url:
            return None

        try:
            with open(upload_file_path, 'rb') as file_data:
                data = {'filesize': str(file_size), 'name': file_name}
                files = {'file': (file_name, file_data)}
                json_data = await get_response_async(upload_url, data=data, files=files, return_json=True)
                log.info(f'上传文件结果：{json_data}')
                return json_data
        except Exception as e:
            log.error('上传文件失败：' + str(e))
            return None
