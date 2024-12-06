# _*_ coding : UTF-8 _*_
# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/10 12:29
# 文件名称： xunlei_base.py
# 项目描述： 迅雷登录等基础操作
# 开发工具： PyCharm
import time
import httpx
import random
import hashlib
import asyncio
import inspect
import aiofiles
import bencodepy
from pathlib import Path
from xiaoqiangclub.config.log_config import log
from typing import (Optional, Dict, Union, List)
from xiaoqiangclub.utils.network_utils import get_random_ua
from xiaoqiangclub.api.xunlei._get_captcha_sign import get_pub_key_sign

UA = get_random_ua(system_type='windows')


class XunleiBase:
    def __init__(self, username: str, password: str):
        """
        Xunlei API（微信公众号：XiaoqiangClub）
        推荐使用async with 语句，确保在函数结束时自动关闭客户端。
        """

        self.common: Dict[Union[str, Dict]] = {
            "username": username,
            "password": password,
            "is_login": False  # 登录状态
        }
        self.log = log
        self.ua = random.choice(UA)  # 随机选择一个UA

    async def get_response(self, url: str, headers: dict = None, patch: bool = False, params: dict = None,
                           data: dict = None, return_json: bool = True, return_response: bool = False,
                           post: bool = False, caller: str = None, timeout: int = 10) -> Optional[Union[Dict, str]]:
        """
        迅雷API中发送请求并返回响应。

        :param url: 请求的 URL
        :param headers: 更新 headers，默认为 None
        :param patch: 是否使用 patch 请求，默认为 False
        :param params: GET 请求的查询参数，默认为 None
        :param data: POST 请求的数据，默认为 None
        :param return_json: 是否返回 JSON 格式的响应，默认为 True，False 则返回response.text
        :param return_response: 是否直接返回 response，默认为 False
        :param caller: 调用者名称，默认为 None
        :param post: 是否使用 POST 请求，默认为 False
        :param timeout: 请求超时时间，默认为 10 秒
        :return: 响应内容（JSON 或文本）
        """
        caller = caller or inspect.currentframe().f_back.f_code.co_name

        last_headers = {"User-Agent": self.ua}  # 添加 随机User-Agent
        if headers:
            last_headers.update(headers)

        try:
            async with httpx.AsyncClient() as client:
                if data or post:
                    if patch:
                        response = await client.patch(url, headers=headers, json=data, params=params, timeout=timeout)
                    else:
                        # 迅雷默认使用的是json格式，所以这里直接用json参数发送
                        response = await client.post(url, headers=headers, json=data, params=params, timeout=timeout)
                else:
                    if patch:
                        response = await client.patch(url, headers=headers, params=params, timeout=timeout)
                    else:
                        response = await client.get(url, headers=headers, params=params, timeout=timeout)

                if return_response:
                    return response

                if response.status_code == 200:
                    self.log.debug(
                        f'[{caller}] 请求方式：{response.request.method}，响应状态码: {response.status_code}，响应内容:{response.text}')

                    if return_json:
                        try:
                            return response.json()
                        except ValueError as json_error:
                            self.log.error(f"JSON 解码失败: {json_error}")
                            return None
                    return response.text
                else:

                    self.log.debug(
                        f'[{caller}] 请求方式：{response.request.method}，响应状态码: {response.status_code}，headers：{headers}，params：{params}，data：{data}，响应内容:{response.text}')
                    return None

        except httpx.RequestError as req_err:
            self.log.debug(f'[{caller}] 请求失败: {req_err}')
            return None
        except Exception as e:
            self.log.debug(f'[{caller}] 发生未知错误: {e}')
            return None

    async def __get_login_device_id(self) -> Optional[str]:
        """
        初始化生成登入设备的 device_id（也就是我们程序的虚拟ID），需要和远程的下载设备 device_id 区分开。

        :return:
        """
        url = "https://xluser-ssl.xunlei.com/risk"
        params = {
            "cmd": "report"
        }
        data = {  # 好像可以直接复用这个 data，以后有空再去写生成函数
            "xl_fp_raw": "53793f98c0f944f0837946d9d694c55b",
            "xl_fp": "dfe57c652a6400764d825dcfb9ea1e17",
            "version": 2,
            "xl_fp_sign": "c8f4a425a1cfd1d8029b0151735d3d7a"
        }
        json_data = await self.get_response(url=url, params=params, data=data)

        if json_data:
            device_sign = json_data.get('deviceid')

            login_device_id = device_sign.split('.')[-1][:32]
            self.common['login_device_id'] = login_device_id  # 登录设备ID：也就是我们现在程序的 device_id
            self.log.debug(f'生成虚拟device_id（用于登录）: {login_device_id}')

            return login_device_id
        else:
            self.log.error('生成设备ID（device_id）失败！')
            return None

    async def __get_captcha_token_for_login(self) -> Optional[str]:
        """
        获取验证码 captcha_token，用于登录，用于登录时："expires_in": 300

        :return: captcha_token 或 None
        """
        # 生成 device_id
        login_device_id = await self.__get_login_device_id()

        url = "https://xluser-ssl.xunlei.com/v1/shield/captcha/init"
        data = {
            "client_id": "XW5SkOhLDjnOZP7J",
            "action": "POST:/v1/auth/signin",
            "device_id": login_device_id,
            # "captcha_token": "xiaoqiangclub",  # 自定义任意值。可以省略
            "meta": {
                "username": self.common.get('username')
            }
        }
        json_data = await self.get_response(url=url, data=data)
        if json_data:
            captcha_token = json_data.get('captcha_token')
            self.log.debug(f'获取验证码(captcha_token): {captcha_token}')
            return captcha_token
        else:
            self.log.error('获取验证码(captcha_token)失败，请检查账号密码是否正确！')
            return None

    async def login(self) -> Optional[Dict]:
        """
        登录获取 bearer_access_token，并返回相关数据

        :return: 登录后的数据
        """
        # 判断是否已经登录
        if self.common.get('is_login'):
            return

        self.log.info(f'登录/重新登陆：{self.common.get("username")}...')

        captcha_token = await self.__get_captcha_token_for_login()

        headers = {
            "x-captcha-token": captcha_token
        }
        url = "https://xluser-ssl.xunlei.com/v1/auth/signin"

        data = {
            "username": self.common.get('username'),
            "password": self.common.get('password'),
            "client_id": "XW5SkOhLDjnOZP7J"
        }

        json_data = await self.get_response(url=url, headers=headers, data=data)

        if json_data:
            # 添加登入状态：一定要第一时间添加，否则后面程序会出现死循环
            self.common['is_login'] = True

            # 保存复用数据
            self.common['access_token'] = json_data.get('access_token')
            self.common['user_id'] = json_data.get('user_id')

            self.log.debug(f'登录成功，初始化数据：{self.common}')
            return self.common
        else:
            # 报错，确保登入账号和密码正确
            self.log.error(
                f"登录失败!请检查账号：{self.common.get('username')} 密码：{self.common.get('password')} 是否正确。")
            return None

    async def __get_token_code(self) -> Optional[str]:
        """
        获取刷新令牌 __refresh_access_token 需要用的code参数

        :return:
        """
        # 判断是否已经登录
        await self.login()

        for _ in range(2):  # 尝试2次
            self.log.debug('获取刷新令牌 __refresh_access_token 需要用的参数code...')
            access_token = self.common.get('access_token')

            headers = {"authorization": f"Bearer {access_token}"}
            url = "https://xluser-ssl.xunlei.com/v1/user/authorize"
            data = {
                "client_id": "Yd0uSVGrNJhCC2oE",
                "response_type": "code",
                "redirect_uri": "https://pan.xunlei.com/remote/login",
                "state": "state-cjho52konov",
                "scope": "profile offline pan sso user",
                "code_challenge": "_41Tnnw5MF4X8dlZ1XDul8SkCZbUuWOWwiPFMTHFieM",
                "code_challenge_method": "S256",
                "sign_out_uri": "https://pan.xunlei.com/remote/signout/?sso_sign_out="
            }

            json_data = await self.get_response(url=url, headers=headers, data=data)
            if json_data:
                token_code = json_data.get('code')
                self.common['token_code'] = token_code
                return token_code

        self.log.error('刷新令牌 __refresh_access_token 需要用的参数code 获取失败！')
        return None

    async def __refresh_captcha_token(self, caller: str = None) -> Optional[str]:
        """
        刷新captcha_token验证码，用于登录后刷新，执行任务："expires_in": 300

        :param caller: 调用者名称
        :return: captcha_token 或 None
        """
        caller = caller or inspect.currentframe().f_back.f_code.co_name
        self.log.debug(f'[{caller}] 刷新 captcha_token 验证码...')

        login_device_id = self.common.get('login_device_id')
        if not login_device_id:
            await self.login()  # 生成 device_id
            login_device_id = self.common.get('login_device_id')  # 刷新

        # 获取时间戳精确到毫秒
        timestamp = str(int(time.time() * 1000))
        # 获取公钥的签名
        captcha_sign = await get_pub_key_sign(login_device_id=login_device_id, timestamp=timestamp)
        url = "https://xluser-ssl.xunlei.com/v1/shield/captcha/init"

        data = {
            "client_id": "Yd0uSVGrNJhCC2oE",
            # "client_id": "Xqp0kJBXWhwaTpB6",  # 云盘登录

            "action": "GET:CAPTCHA_TOKEN",  # 还可以设置为"PATCH:/drive/v1/task"，还没找出来具体作用
            "device_id": self.common.get('login_device_id'),
            "meta": {
                "user_id": self.common.get('user_id'),
                "user_name": self.common.get('username'),
                "client_version": "2.9.0",
                "package_name": "pan.xunlei.com",
                "timestamp": timestamp,
                "captcha_sign": captcha_sign
            }
        }

        json_data = await self.get_response(url=url, data=data)

        if json_data:
            captcha_token = json_data.get('captcha_token')
            self.common['captcha_token'] = captcha_token
            return captcha_token
        else:
            self.log.error('刷新 captcha_token 失败！')

    async def __refresh_access_token(self, caller: str = None) -> Optional[str]:
        """
        获取access_token令牌："expires_in": 43200

        :param caller: 调用者名称
        :return:包含access_token、refresh_token等
        """
        caller = caller or inspect.currentframe().f_back.f_code.co_name
        self.log.debug(f'[{caller}] 刷新 access_token 令牌...')

        token_code = self.common.get('token_code')
        if not token_code:
            token_code = await self.__get_token_code()
            if not token_code:
                self.log.error('刷新 access_token 令牌失败！')
                return None

        url = "https://xluser-ssl.xunlei.com/v1/auth/token"
        data = {
            "code": token_code,
            "grant_type": "authorization_code",
            "code_verifier": "tsj8U88I1q4tyQOlfUZieLBzuv54EKFk",
            "redirect_uri": "https://pan.xunlei.com/remote/self.login",
            "client_id": "Yd0uSVGrNJhCC2oE"
            # "client_id": "Xqp0kJBXWhwaTpB6",  # 云盘登录
        }
        json_data = await self.get_response(url=url, data=data)
        if json_data:
            # 更新令牌数据
            self.common['access_token'] = json_data.get('access_token')
            return json_data.get('access_token')
        else:
            self.log.error('刷新 access_token 令牌失败！')
            return None

    async def __refresh(self, caller: str = None) -> Optional[List]:
        """
        刷新令牌和刷新验证码
        access_token 令牌："expires_in": 43200
        captcha_token 验证码："expires_in": 300
        账号第一次登入后需要刷新一次 access_token 令牌。

        :param caller: 调用者名称
        """
        caller = caller or inspect.currentframe().f_back.f_code.co_name
        access_token = await self.__refresh_access_token(caller)
        captcha_token = await self.__refresh_captcha_token(caller)

        return [access_token, captcha_token]

    async def fetch_login_after(self, url: str, headers: dict = None, patch: bool = False,
                                params: dict = None, data: dict = None, return_json: bool = True,
                                return_response: bool = False, post: bool = False, timeout: int = 10,
                                max_retries=2, sleep_time: int = None) -> Optional[Union[Dict, httpx.Response]]:
        """
        登录后，发送请求的模板，含刷新令牌/刷新验证码

        :param url: 请求地址
        :param headers: 更新 headers
        :param patch: 是否为PATCH请求，默认为False
        :param params: 请求参数
        :param data: 请求数据
        :param return_json: 返回 JSON 数据，默认为True
        :param return_response: 是否直接返回 response，默认为 False
        :param post: 是否为POST请求，默认为False
        :param timeout: 请求超时时间，默认为10秒
        :param max_retries: 最大重试次数，默认为2，超过此次数则返回None
        :param sleep_time: 延迟时间，默认为None
        :return: 请求响应的 JSON 数据，如果请求失败则返回 None
        """
        await self.login()

        caller = inspect.currentframe().f_back.f_code.co_name  # 获取调用函数名称

        # 从common中获取access_token和captcha_token
        access_token = self.common.get('access_token')
        captcha_token = self.common.get('captcha_token')

        for retry_count in range(max_retries + 2):

            last_headers = {
                "authorization": f"Bearer {access_token}",
                "x-captcha-token": captcha_token,
                # "x-client-id": "Yd0uSVGrNJhCC2oE",
                "x-device-id": self.common.get('login_device_id')
            }
            if headers:
                last_headers.update(headers)

            json_data_or_response = await self.get_response(url=url, headers=last_headers, patch=patch, params=params,
                                                            data=data, return_json=return_json,
                                                            return_response=return_response,
                                                            post=post, caller=caller, timeout=timeout)

            if isinstance(json_data_or_response, httpx.Response) and json_data_or_response.status_code == 200:
                return json_data_or_response

            # PATCH请求，得到一个字典：一般执行暂停、开始等操作会返回一个{}空字典
            if patch and isinstance(json_data_or_response, dict):
                return json_data_or_response

            if json_data_or_response and not return_response:
                return json_data_or_response

            if retry_count == 0:
                captcha_token = await self.__refresh_captcha_token(caller)
            elif retry_count == 1:
                access_token, captcha_token = await self.__refresh(caller)
            elif retry_count == 2:
                if return_response:  # 防止因为验证码失效导致获取响应失败
                    return json_data_or_response

                # 将登陆状态改为未登录
                self.common['is_login'] = False
                await self.login()
                access_token = self.common.get('access_token')
                captcha_token = await self.__refresh_captcha_token(caller)

            if sleep_time:
                await asyncio.sleep(sleep_time)

        return None

    @staticmethod
    async def generate_number_string_list(count: int) -> List[str]:
        """
        生成指定数量的数字字符串列表

        :param count: 要生成的数字字符串的数量
        :return: 数字字符串列表
        """
        if count < 0:
            raise ValueError("Count must be a non-negative integer")

        return [str(i) for i in range(count)]

    @staticmethod
    async def split_path(path: str, change_to_lower=False, only_get_folder_name=True) -> List[str]:
        """
        分割路径，将路径转换为列表
        :param path: 路径
        :param change_to_lower: 是否将路径转换为小写，默认为False
        :param only_get_folder_name: 是否只获取文件夹名称，默认为True
        :return: List[str]
        """
        p = Path(path)
        parts = [str(part) for part in p.parts]

        if only_get_folder_name:
            # 去除路径中的 '/'、'\' 和 '\\，并且去除空字符串
            parts = [part for part in parts if part and part != '/' and part != '\\' and part != '\\\\']
        if change_to_lower:
            parts = [part.lower() for part in parts]
        return parts

    @staticmethod
    async def format_sub_file_index(sub_file_index: List[str]) -> str:
        """
        格式化子文件索引，将子文件索引转换为迅雷支持的格式，例如："0":第一集，或只有一集，"0-15"：第1-16集，"0-5,7-13,15"：第1-6集，第8-14集，第16集。

        :param sub_file_index: 子文件索引（从1开始），例如：['1', '2']
        :return:
        """
        # 转换为整数并排序
        indices = sorted(int(i) - 1 for i in sub_file_index)  # 从1开始转换为从0开始

        ranges = []
        start = indices[0]
        end = indices[0]

        for i in range(1, len(indices)):
            if indices[i] == end + 1:  # 如果是连续的
                end = indices[i]
            else:  # 如果不连续，记录当前范围
                if start == end:
                    ranges.append(f"{start}")
                else:
                    ranges.append(f"{start}-{end}")
                start = end = indices[i]  # 更新开始和结束索引

        # 添加最后一个范围
        if start == end:
            ranges.append(f"{start}")
        else:
            ranges.append(f"{start}-{end}")

        return ",".join(ranges)

    async def get_user_info(self) -> Optional[dict]:
        """
        获取需要用到的用户信息

        :return:
        """
        # 判断是否已经登录
        await self.login()

        self.log.debug(f'获取 {self.common.get("username")} 的用户信息...')
        access_token = self.common.get('access_token')
        # 运行2次
        for _ in range(2):
            headers = {"authorization": f"Bearer {access_token}"}
            url = "https://xluser-ssl.xunlei.com/v1/user/me"
            json_data = await self.get_response(url=url, headers=headers)

            if json_data:
                common_data = {
                    'account_status': json_data.get('status'),  # 账号状态
                    'phone_number': json_data.get('phone_number'),  # 手机号码，中间6位隐藏
                    'is_vip': json_data.get('vip_info')[0].get('is_vip') != "0",  # 是否为会员
                }
                self.common.update(common_data)
                self.log.info(f'获取到 {self.common.get("username")} 的用户信息：{json_data}')

                return json_data
            else:
                self.log.debug('令牌已过期，刷新令牌...')
                access_token = await self.__refresh_access_token()

    async def get_download_url_info(self, task_url: str, return_all: bool = False) -> Optional[Dict]:
        """
        获取下载url的信息：文件大小、名称等

        :param return_all: 是否返回所有信息
        :param task_url: 任务url链接的详情
        :return:
        """
        # 判断是否已经登录
        await self.login()

        self.log.debug(f'获取 {task_url} 的下载任务信息...')
        api_url = "https://api-pan.xunlei.com/drive/v1/resource/list"
        data = {
            "urls": task_url,
            "page_size": 2000
        }

        json_data = await self.fetch_login_after(url=api_url, data=data)
        if not json_data:
            return None

        if return_all:
            return json_data

        try:
            # 整理返回数据
            resources: dict = json_data.get('list', {}).get('resources', [])[0]
            meta: dict = resources.get('meta')
            _dir = resources.get('dir', {})
            files = _dir.get('resources', []) if _dir else []

            return {
                'task_name': resources.get('name'),  # 外层文件夹名称
                'task_size': resources.get('file_size'),  # 任务总容量
                'file_count': resources.get('file_count'),  # 文件数量
                'files': files,  # 文件列表
                'task_url': meta.get('url')  # 文件下载链接
            }
        except Exception as e:
            self.log.error(f'获取 {task_url} 的下载任务信息失败: {e}')
            return None

    async def parse_torrent(self, torrent_file_path) -> List[str]:
        """
        解析torrent文件，获取磁链和资源名称

        :param torrent_file_path: .torrent文件路径
        :return: 磁链和资源名称
        """
        # 异步读取 .torrent 文件
        async with aiofiles.open(torrent_file_path, 'rb') as f:
            torrent_data = await f.read()

        # 解析 .torrent 文件
        torrent_dict = bencodepy.decode(torrent_data)

        # 获取 info 部分并计算 info_hash
        info = bencodepy.encode(torrent_dict.get(b'info', {}))
        info_hash = hashlib.sha1(info).hexdigest()

        # 获取资源名称（电影名）
        name = torrent_dict.get(b'info', {}).get(b'name', b'').decode('utf-8')  # 解码为字符串

        magnet_link = f"magnet:?xt=urn:btih:{info_hash}"
        self.log.debug(f'{torrent_file_path} 资源名称为：{name}，磁链为： {magnet_link}')
        return [magnet_link, name]  # 返回磁力链接和名称
