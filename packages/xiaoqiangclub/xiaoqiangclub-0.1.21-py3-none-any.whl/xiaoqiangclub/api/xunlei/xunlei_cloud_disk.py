# _*_ coding : UTF-8 _*_
# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/10 13:59
# 文件名称： xunlei_cloud_disk.py
# 项目描述： 迅雷云盘（https://pan.xunlein.com）的接口
# 开发工具： PyCharm
import os
import re
import hmac
import json
import time
import httpx
import base64
import hashlib
import asyncio
import tempfile
import aiofiles
from pathlib import Path
from datetime import datetime
from typing import (Optional, Dict, List, Union)
from xiaoqiangclub.api.xunlei.xunlei_base import XunleiBase


class XunleiCloudDisk(XunleiBase):
    def __init__(self, username: str, password: str):
        """
        Xunlei云盘 API（微信公众号：XiaoqiangClub）

        :param username: 用户名
        :param password: 密码
        """
        super().__init__(username=username, password=password)

    async def yunpan_create_share_link(self, yunpan_resource_path: str, with_passcode_in_link: bool = True,
                                       extraction_times: int = -1, valid_days: int = -1,
                                       return_raw_data: bool = False) -> Optional[Union[str, dict]]:
        """
        获取云盘分享链接

        :param yunpan_resource_path: 云盘资源路径
        :param with_passcode_in_link: 是否在链接中包含提取码
        :param extraction_times: 提取次数（1-20），-1表示无限制
        :param valid_days: 有效天数（1-7），-1表示永久有效
        :param return_raw_data: 是否返回所有原始数据，默认为False，只返回分享链接
        :return:
        """
        await self.login()

        # 获取文件id
        resource_info = await self.__yunpan_get_resource_info(yunpan_resource_path)

        if not resource_info:
            return

        # 校验提取次数
        if isinstance(extraction_times, int):
            if extraction_times != -1:
                extraction_times = max(1, min(extraction_times, 20))
        else:
            raise TypeError("extraction_times must be an integer.")

        # 校验有效天数
        if isinstance(valid_days, int):
            if valid_days != -1:
                valid_days = max(1, min(valid_days, 7))
        else:
            raise TypeError("valid_days must be an integer.")

        data = {
            "file_ids": [
                resource_info.get('id')  # 文件id
            ],
            "share_to": "copy",
            "params": {
                "subscribe_push": "false",
                "WithPassCodeInLink": "true" if with_passcode_in_link else "false"  # 确保转换为字符串
            },
            "title": "云盘资源分享",
            "restore_limit": str(extraction_times),  # 提取次数
            "expiration_days": str(valid_days)  # 有效天数
        }

        json_data = await self.fetch_login_after(url="https://api-pan.xunlei.com/drive/v1/share", data=data)
        if json_data:
            if return_raw_data:
                return json_data

            share_link = json_data.get('share_url') + "?pwd=" + json_data.get('pass_code')
            self.log.info(f'获取到 {yunpan_resource_path} 的云盘分享链接：{share_link}')
            return share_link

        else:
            self.log.error(f'获取 {yunpan_resource_path} 的云盘分享链接失败！')

    async def __yunpan_get_dir_map(self, parent_folder_id: str, current_path: str, file_handle) -> Optional[list]:
        """
        获取迅雷云盘指定文件夹下的文件夹和文件信息，仅获取一级文件夹和文件，不递归。

        :param parent_folder_id: 父文件夹id
        :param current_path: 当前路径
        :param file_handle: 文件处理器
        :return:
        """
        info_list = await self.__yunpan_get_dir_info(parent_folder_id)
        if info_list is None:
            self.log.error(f'获取 {parent_folder_id} 下的目录和文件信息失败！')
            return None

        folder_list = []  # 存放文件夹信息
        save_list = []  # 存放文件信息
        for info in info_list:
            folder_path = current_path + '/' + info.get('name')  # 拼接路径
            info['real_path'] = folder_path  # 真实路径

            if info.get('kind') == 'drive#folder':
                # 保存路径
                folder_list.append(info)

            save_list.append(info)

        if save_list:  # 异步保存文件信息
            await self.__save_to_file(save_list, file_handle)

        return folder_list

    async def __save_to_file(self, data_list: List[Dict], file_handle) -> None:
        """
        异步保存数据到文件

        :param data_list: 数据列表
        :param file_handle: 文件处理器
        :return:
        """
        self.log.debug(f'保存云盘资源信息到：{file_handle.name}')
        for data in data_list:
            try:
                await file_handle.write(json.dumps(data, ensure_ascii=False) + '\n')
            except Exception as e:
                self.log.error(f'保存云盘资源信息 {data} 到文件时出错：{e}')

    async def __traverse_folder_and_save(self, parent_folder_id: str, current_path: str, file_handle) -> None:
        """
        递归遍历文件夹，并保存文件信息

        :param parent_folder_id: 父文件夹id
        :param current_path: 当前路径
        :param file_handle: 文件处理器
        :return:
        """
        folder_list = await self.__yunpan_get_dir_map(parent_folder_id, current_path, file_handle)

        if not folder_list:
            return None

        self.log.debug(f'开始遍历 {current_path} 下的文件夹，不启用并发')
        for folder in folder_list:
            await self.__traverse_folder_and_save(folder['id'], folder['real_path'], file_handle)

    async def yunpan_get_folder_map(self, folder_path: str, save_path: str) -> None:
        """
        导出迅雷云盘完整目录结构到本地指定文件，便于资源搜索

        :param folder_path: 迅雷云盘文件夹路径，形如：/我的资源/电影/2023
        :param save_path: 保存路径，一行一个字典的保存到文件，所以处理的时候以行为单位进行读取。例如：async for line in file_handle:
        :return:
        """
        await self.login()
        start_time = time.time()
        folder_info = await self.__yunpan_get_resource_info(folder_path)

        self.log.info(f'开始导出云盘目录结构，保存路径：{save_path}')
        async with aiofiles.open(save_path, 'w', encoding='utf-8') as file_handle:
            await self.__traverse_folder_and_save(folder_info.get('id'), folder_path, file_handle)

        self.log.info(f'本次导出云盘数据已保存到 {save_path}，任务共耗时：{int(time.time() - start_time)} 秒')

    async def __yunpan_get_map(self, save_path: str) -> None:
        """
        导出迅雷云盘完整目录结构到本地指定文件，便于资源搜索

        :param save_path: 保存路径
        :return:
        """
        await self.login()
        start_time = time.time()

        self.log.info(f'开始导出云盘目录结构，保存路径：{save_path}')
        async with aiofiles.open(save_path, 'w', encoding='utf-8') as file_handle:
            await self.__traverse_folder_and_save("", "", file_handle)

        self.log.info(f'本次导出云盘数据已保存到 {save_path}，任务共耗时：{int(time.time() - start_time)} 秒')

    async def __yunpan_load_local_map(self, file_path: str) -> Optional[List[Dict]]:
        """
        从本地文件加载云盘map数据，数据是用于搜索云盘资源用的

        :param file_path: 保存云盘map的本地文件路径
        :return:
        """
        self.log.debug(f'开始加载本地数据：{file_path}')
        if not os.path.exists(file_path):
            return None

        async with aiofiles.open(file_path, 'r', encoding='utf-8') as file_handle:
            data = []
            async for line in file_handle:
                data.append(json.loads(line))
        return data

    async def yunpan_search_resources(self, query: str, exact_match: bool = False, force_update: bool = False,
                                      auto_update: bool = True, file_path: str = None) -> List[Dict]:
        """
        搜索迅雷云盘资源，这里不能使用并发，服务器不允许

        :param query: 搜索关键字
        :param exact_match: 是否精确匹配：文件名和query 完全一致，否则为文件名包含query。默认为False
        :param force_update: 是否强制更新数据：True 则直接获取最新数据，False 则使用本地数据
        :param auto_update: 当使用本地数据没有搜索到结果时，是否自动更新数据，True 则自动更新，False 则不更新，默认为 True
        :param file_path: 导出迅雷云盘map数据到本地文件路径，默认为 "./xunlei_yunpan_resources_{username}.json"
        :return:
        """
        await self.login()

        self.log.debug(f'开始搜索云盘资源，搜索关键字：{query}')
        if not file_path:
            file_path = f'./xunlei_yunpan_resources_{self.common.get("username")}.json'

        # 如果 force_update 为 True，直接获取最新数据
        if force_update:
            await self.__yunpan_get_map(file_path)

        data = await self.__yunpan_load_local_map(file_path)

        # 如果本地数据为空，且没有强制更新，则获取最新数据
        if not data and not force_update:
            self.log.info('本地数据为空，尝试从云盘导出最新数据...')

            await self.__yunpan_get_map(file_path)
            data = await self.__yunpan_load_local_map(file_path)
            if not data:
                return []

        results = []
        for item in data:
            name = item.get('name', '')
            if (exact_match and name == query) or (not exact_match and query in name):
                results.append(item)

        # 如果第一次搜索没有结果，更新数据后再次搜索
        if not results and not force_update and auto_update:
            self.log.debug('本地数据没有搜索到结果，尝试更新本地数据...')
            await self.__yunpan_get_map(file_path)
            data = await self.__yunpan_load_local_map(file_path)
            for item in data:
                name = item.get('name', '')
                if (exact_match and name == query) or (not exact_match and query in name):
                    results.append(item)

        self.log.info(f'搜索云盘资源完成，共找到 {len(results)} 个结果')
        return results

    async def __yunpan_get_next_page_info(self, next_page_token: str, params: dict):
        """
        获取云盘下一页信息

        :param next_page_token: 下一页的token
        :param params: 请求参数
        :return:
        """
        self.log.debug('正在获取云盘下一页信息...')
        params['page_token'] = next_page_token
        return await self.fetch_login_after(url="https://api-pan.xunlei.com/drive/v1/files", params=params)

    async def __yunpan_get_dir_info(self, parent_folder_id: str = "", return_raw_data: bool = False,
                                    filters: str = None) -> Optional[List[Dict]]:
        """
        获取云盘文件夹信息：文件/目录id等

        :param parent_folder_id: 父级目录的ID，默认为空字符串""：获取云盘顶级根目录的 folder_id
        :param return_raw_data: 是否返回原始数据，默认为False，只返回主要信息
        :param filters: 过滤条件，默认为None，使用默认过滤条件
        :return:
        """
        self.log.debug(f'正在获取云盘父级目录ID：{parent_folder_id} 的文件夹信息...')

        params = {
            "parent_id": parent_folder_id,
            "filters": "{\"phase\":{\"eq\":\"PHASE_TYPE_COMPLETE\"},\"trashed\":{\"eq\":false}}",
            "with_audit": "true",
            "thumbnail_size": "SIZE_SMALL",
            "limit": "50"
        }
        if filters:
            params['filters'] = filters

        json_data = await self.fetch_login_after(url="https://api-pan.xunlei.com/drive/v1/files", params=params)
        if not json_data:
            self.log.error(f'获取云盘父级目录ID：{parent_folder_id} 的文件夹信息失败')
            return None

        # 获取下一页的 next_page_token
        file_list = json_data.get('files', [])
        next_page_token = json_data.get('next_page_token')
        while True:
            if not next_page_token:
                break

            next_page_info = await self.__yunpan_get_next_page_info(next_page_token, params)

            if next_page_info:
                next_page_token = next_page_info.get('next_page_token')
                file_list.extend(next_page_info.get('files', []))
            else:
                break

        if return_raw_data:
            return file_list

        yunpan_dirs = []
        for file in file_list:
            yunpan_dirs.append({
                "name": file.get('name'),  # 目录名（我的转存）
                "id": file.get('id'),  # 目录或文件的ID（VNv5Ol2sxliNst19L1IRVi4OA1）
                "parent_id": file.get('parent_id'),  # 父级目录ID
                "folder_type": file.get('folder_type'),  # 目录类型：RESTORE、DOWNLOAD、NORMAL
                "kind": file.get('kind'),  # 文件类型：drive#folder、drive#file
                "writable": file.get('writable'),  # 是否可写
                "size": file.get('size'),  # 文件大小，单位为字节（570782536），0表示文件夹
                "hash": file.get('hash'),  # 文件哈希值（F71FD59E86C58BD2BF5309A6C53763F8D397928C），用于校验文件
            })

        self.log.debug(f'获取云盘父级目录ID：{parent_folder_id} 的文件夹信息 {yunpan_dirs}')
        return yunpan_dirs

    async def yunpan_recycle_bin_clear(self, files_name: Union[str, List[str]] = None, fuzzy_search: bool = False,
                                       delete_all: bool = False) -> Optional[bool]:
        """
        清空回收站或删除指定文件

        :param files_name: 需要删除的文件名/文件夹名，支持单个字符串或列表
        :param fuzzy_search: 是否模糊搜索，默认为False，精确搜索
        :param delete_all: 是否删除全部文件，默认为False，仅删除指定文件/文件夹
        :return: True: 清空回收站成功，False: 清空回收站失败，None: 无回收站文件
        """
        files = await self.__yunpan_get_dir_info("*", filters='{"trashed":{"eq":true}}')

        if not files:
            self.log.info('回收站为空，无需清理...')
            return None

        # 处理文件名参数，确保其为列表类型
        if files_name and isinstance(files_name, str):
            files_name = [files_name]

        # 获取需要删除的文件ID
        def should_delete(file):
            if delete_all:
                return True
            if files_name:
                return any(name in file['name'] for name in files_name) if fuzzy_search else file['name'] in files_name
            return False

        files_id = [file['id'] for file in files if should_delete(file)]

        if not files_id:
            self.log.warn(f'回收站中没有找到您需要删除的文件：{files_name}')
            return None

        data = {
            "ids": files_id,
            "space": ""
        }

        json_data = await self.fetch_login_after(url="https://api-pan.xunlei.com/drive/v1/files:batchDelete", data=data)
        if json_data:
            self.log.info(f'回收站清空成功，共删除 {len(files_id)} 个文件')
            return True

        self.log.error('回收站清空失败！')
        return False

    from typing import Union, List

    async def yunpan_recycle_bin_restore(self, files_name: Union[str, List[str]] = None, save_path: str = None,
                                         fuzzy_search: bool = False, restore_all: bool = False) -> Optional[bool]:
        """
        还原云盘回收站中的文件。

        :param files_name: 需要还原的文件名/文件夹名，支持单个字符串或列表。
        :param save_path: 还原到云盘的路径，默认为None，根目录
        :param fuzzy_search: 是否启用模糊搜索，默认为False，使用精确搜索。
        :param restore_all: 是否还原全部文件，默认为False，仅还原指定文件/文件夹。
        :return: True表示还原成功，False表示还原失败， None表示没有找到文件。
        """
        files = await self.__yunpan_get_dir_info("*", filters='{"trashed":{"eq":true}}')

        # 处理文件名参数，确保其为列表类型
        if files_name and isinstance(files_name, str):
            files_name = [files_name]

        # 获取需要还原的文件ID
        def should_restore(file):
            if restore_all:
                return True
            if files_name:
                return any(name in file['name'] for name in files_name) if fuzzy_search else file['name'] in files_name
            return False

        files_id = [file['id'] for file in files if should_restore(file)]

        if not files_id:
            self.log.warn(f'回收站中没有找到您需要还原的文件：{files_name}')
            return None

        # 创建并发任务进行文件还原
        tasks = [
            self.fetch_login_after(url=f"https://api-pan.xunlei.com/drive/v1/files/{file_id}/untrash",
                                   data={}, patch=True)
            for file_id in files_id
        ]

        try:
            await asyncio.gather(*tasks)
            self.log.info('文件还原完成')
            if save_path:  # 移动文件到指定路径
                await self.__yunpan_file_manage("", save_path, "batchMove", files_id)
            return True
        except Exception as e:
            self.log.error(f'文件还原过程中出现错误: {e}')
            return False

    async def __yunpan_get_resource_info(self, target_folder: str) -> Optional[Dict]:
        """
        获取云盘指定文件/目录信息id 等

        :param target_folder: 目标文件/文件夹夹名（例如：我的转存）
        :return:
        """
        await self.login()

        # 将目标文件夹路径转换为列表
        target_parts = await self.split_path(target_folder, change_to_lower=True)

        parent_folder_id = ""  # 用于保存当前目录的ID
        match_dir_info: Optional[Dict] = None  # 匹配到的路径信息

        for part in target_parts:
            # 获取顶级目录的 folder_id
            root_dirs = await self.__yunpan_get_dir_info(parent_folder_id)
            if root_dirs:
                matched = False  # 标记当前层级是否找到匹配
                for dir in root_dirs:
                    if part == dir.get('name').strip().lower():  # 转换为小写
                        parent_folder_id = dir.get('id')
                        matched = True
                        match_dir_info = dir
                        break  # 找到后跳出当前层级的循环

                # 如果当前层级没有找到匹配，返回 None
                if not matched:
                    self.log.error(f'在云盘未找到路径：{target_folder}，请检查路径是否正确！')
                    return None
            else:
                self.log.error(f'在云盘未找到路径：{target_folder}，请检查路径是否正确！')
                return None

        self.log.debug(f"获取到 {target_folder} 的信息：{match_dir_info}")
        match_dir_info['real_path'] = target_folder
        return match_dir_info

    async def yunpan_rename(self, old_path: str, new_name: str) -> Optional[bool]:
        """
        重命名迅雷云盘文件或文件夹

        :param old_path: 需要重命名的云盘文件/文件夹路径
        :param new_name: 新的文件/文件夹名称：只需要填写文件/文件夹名称，不包含路径
        :return:
        """
        await self.login()

        # 获取文件/目录信息
        path_info = await self.__yunpan_get_resource_info(old_path)

        if not path_info:
            return None

        path_id = path_info.get('id')
        parent_id = path_info.get('parent_id')
        url = f'https://api-pan.xunlei.com/drive/v1/files/{path_id}'
        data = {
            "name": new_name,
            # "space": ""
        }

        await self.fetch_login_after(url=url, data=data, patch=True)  # 重命名
        # 验证是否重命名成功
        file_list = await self.__yunpan_get_dir_info(parent_id)  # 上一级文件列表
        if file_list:
            for file in file_list:
                if file.get('id') == path_id and file.get('name') == new_name:
                    self.log.info(
                        f"云盘 {old_path} 重命名为 {old_path.replace(old_path.split('/')[-1], new_name)} 成功！")
                    return True

        self.log.error(f"云盘 {old_path} 重命名为 {old_path.replace(old_path.split('/')[-1], new_name)} 失败！")
        return False

    async def yunpan_get_tasks_history(self, limit: int = 100):
        """
        获取迅雷"云添加"记录

        :param limit: 最多返回的任务数量，默认为 100，None 表示不限制数量
        :return:
        """
        await self.login()

        params = {
            "limit": str(limit),
            "phaseCheck": "false",
            "page_token": "",
            "type": "offline"
        }
        return await self.fetch_login_after(url="https://api-pan.xunlei.com/drive/v1/tasks", params=params)

    async def __yunpan_file_manage(self, old_path: Union[str, List[str]], new_path: str, task_type: str,
                                   path_id_list: Union[str, List[str]] = None) -> Optional[bool]:
        """
        云盘文件/文件夹的管理：移动、复制、彻底删除等

        :param old_path: 需要操作的云盘文件/文件夹路径，可以是单个路径，也可以是多个路径
        :param new_path: 新的文件/文件夹路径
        :param task_type: 操作类型：batchMove、batchCopy、batchDelete
        :param path_id_list: 旧路径对应的id，用于批量操作，如果设置了old_path_id，则 old_path 参数失效，为了兼容可以设置为 ""。
        :return:
        """
        await self.login()

        if isinstance(path_id_list, str):
            path_id_list = [path_id_list]

        if not path_id_list:
            if isinstance(old_path, str):
                old_path = [old_path]

            # 并发获取文件/目录信息
            path_info_list = await asyncio.gather(*[self.__yunpan_get_resource_info(path) for path in old_path])

            # 获取id，去除 None
            path_info_list = list(filter(None, path_info_list))
            path_id_list = [info.get('id') for info in path_info_list]

        if task_type == "batchDelete":
            new_path_info = {'id': 'xiaoqiangclub'}
        else:
            new_path_info = await self.__yunpan_get_resource_info(new_path)

        if not (path_id_list and new_path_info):
            return None

        data = {
            "ids": path_id_list,
            "to": {
                "parent_id": new_path_info.get('id'),
                "space": ""
            },
            "space": ""
        }
        if task_type == "batchDelete":
            data.pop("to")  # 删除 "to" 参数

        json_data = await self.fetch_login_after(url=f"https://api-pan.xunlei.com/drive/v1/files:{task_type}",
                                                 data=data)
        if json_data:
            if task_type == "batchDelete":
                self.log.info(f"云盘 {old_path} 删除成功（有可能是部分成功，请自行查看云盘）！")
            else:
                self.log.info(f"云盘 {old_path} 移动/复制到 {new_path} 成功！")
            return True
        else:
            if task_type == "batchDelete":
                self.log.error(f"云盘 {old_path} 删除失败！")
            else:
                self.log.error(f"云盘 {old_path} 移动/复制到 {new_path} 失败！")
            return False

    async def yunpan_file_move(self, old_path: Union[str, List[str]], new_path: str) -> Optional[bool]:
        """
        移动云盘文件或文件夹

        :param old_path: 需要移动的云盘文件/文件夹路径，可以是单个路径，也可以是多个路径
        :param new_path: 新的文件/文件夹路径
        :return:
        """
        return await self.__yunpan_file_manage(old_path, new_path, "batchMove")

    async def yunpan_file_copy(self, old_path: Union[str, List[str]], new_path: str) -> Optional[bool]:
        """
        复制云盘文件或文件夹

        :param old_path: 需要复制的云盘文件/文件夹路径，可以是单个路径，也可以是多个路径
        :param new_path: 新的文件/文件夹路径
        :return:
        """
        return await self.__yunpan_file_manage(old_path, new_path, "batchCopy")

    async def yunpan_file_delete_forever(self, path: Union[str, List[str]]) -> Optional[bool]:
        """
        永久删除云盘文件或文件夹

        :param path: 需要永久删除的云盘文件/文件夹路径，可以是单个路径，也可以是多个路径
        :return:
        """
        return await self.__yunpan_file_manage(path, "", "batchDelete")

    async def yunpan_file_delete(self, path: Union[str, List[str]], delete_forever: bool = False) -> Optional[bool]:
        """
        删除云盘文件或文件夹

        :param path: 需要删除的云盘文件/文件夹路径，可以是单个路径，也可以是多个路径
        :param delete_forever: 是否永久删除，默认为False
        :return: 删除结果列表，True表示删除成功，False表示删除失败，None表示获取文件/目录信息失败。多任务的时候返回结果仅供参考...
        """
        await self.login()

        if isinstance(path, str):
            path = [path]

        async def move_to_recycle_bin(one_path: str):
            """删除一个文件到回收站"""
            # 获取文件/目录信息id
            path_info = await self.__yunpan_get_resource_info(one_path)

            if not path_info:
                return None

            url = f"https://api-pan.xunlei.com/drive/v1/files/{path_info.get('id')}/trash"
            json_data = await self.fetch_login_after(url=url, data={}, patch=True)
            if json_data:
                self.log.info(f"云盘 {one_path} 删除成功，已放入回收站！")
                return True
            else:
                self.log.error(f"云盘 {one_path} 删除失败！")
                return False

        if delete_forever:
            return await self.yunpan_file_delete_forever(path)
        else:
            del_rets = await asyncio.gather(*[move_to_recycle_bin(one_path) for one_path in path])

            if True in del_rets:
                return True

            elif False in del_rets:
                return False

            return None

    async def yunpan_create_folders(self, folder_name_or_path: str, parent_folder: str = None) -> bool:
        """
        云盘新建文件夹
        如果有同名文件夹，则不创建。支持创建多级文件夹。

        :param folder_name_or_path: 文件夹名或路径，默认在根目录下创建，例如：mydata/data，如果设置了parent_folder，将在parent_folder下创建这个文件夹/路径
        :param parent_folder: 目标文件夹，例如：我的转存，默认为None：新建在根目录
        :return:
        """
        # 判断folder_name_or_path是否为文件夹路径
        if "/" in folder_name_or_path or "\\" in folder_name_or_path:
            folder_name_list = await self.split_path(folder_name_or_path)
        else:
            folder_name_list = [folder_name_or_path]

        temp_list = [parent_folder] if parent_folder else []
        parent_folder_id = None  # 用于记录当前已创建的父文件夹的id

        for folder_name in folder_name_list:
            temp_list.append(folder_name)

            # 判断文件夹是否已经存在
            path_info = await self.__yunpan_get_resource_info('/'.join(temp_list))
            if path_info:
                self.log.info(f"云盘 {'/'.join(temp_list)} 已存在，跳过创建！")
                parent_folder_id = path_info.get('id')  # 更新parent_folder_id
                parent_folder = None  # 更新parent_folder
                continue
            create_ret = await self.__yunpan_create_folder(folder_name, parent_folder=parent_folder,
                                                           parent_folder_id=parent_folder_id)

            if not create_ret:
                self.log.error(f"云盘 新建文件夹 {'/'.join(temp_list)} 失败！")
                return False

            parent_folder_id = create_ret.get('id')  # 更新parent_folder_id
            parent_folder = None  # 更新parent_folder
        return True

    async def __yunpan_create_folder(self, folder_name: str, parent_folder: str = None, parent_folder_id: str = None) -> \
            Optional[Dict]:
        """
        云盘新建文件夹，只支持创建一级文件夹，不支持创建多级文件夹

        :param folder_name: 文件夹名
        :param parent_folder: 父级文件夹，例如：mydata，默认为None：新建在根目录
        :param parent_folder_id: 目标文件夹id
        :return:
        """
        await self.login()

        if not parent_folder_id:
            if parent_folder is None:
                parent_folder_id = ""
            else:
                parent_folder_info = await self.__yunpan_get_resource_info(parent_folder)
                if not parent_folder_info:
                    return None
                parent_folder_id = parent_folder_info.get('id')

        url = "https://api-pan.xunlei.com/drive/v1/files"
        data = {
            "parent_id": parent_folder_id,
            "name": folder_name,
            "kind": "drive#folder",
            "space": ""
        }

        response = await self.fetch_login_after(url=url, data=data, return_response=True)
        json_data = response.json()

        # 获取父目录名称
        if not parent_folder:
            if parent_folder_id:
                dir_info = await self.__yunpan_get_dir_info(parent_folder_id)
                parent_folder = dir_info[0].get('name') if dir_info else None
            else:
                parent_folder = "根目录"

        if response.status_code == 200:
            await asyncio.sleep(1)  # 等待服务器创建成功
            self.log.info(f"在云盘 {parent_folder} 目录下新建文件夹 {folder_name} 成功！")
            file = json_data.get('file')

            return {
                "name": file.get('name'),  # 文件夹名称
                "id": file.get('id'),  # 文件夹id
                "parent_id": file.get('parent_id'),  # 父文件夹id
            }
        else:
            self.log.error(
                f"在云盘 {parent_folder} 目录下创建文件夹 {folder_name} 失败：{json_data.get('error_description')}")
            return None

    async def yunpan_file_or_folder_exists(self, path: str) -> bool:
        """
        判断云盘文件或文件夹是否存在

        :param path: 文件/文件夹路径
        :return:
        """
        await self.login()

        json_data = await self.__yunpan_get_resource_info(path)
        if json_data:
            return True
        return False

    async def yunpan_file_in_folder(self, file_name: str, target_folder: str) -> Optional[bool]:
        """
        判断指定的云盘目录下是否存在指定的文件/文件名

        :param file_name: 文件名(非完整路径，也就是在所有的)
        :param target_folder: 目标文件夹名（例如：我的转存）
        :return:
        """
        # 判断是否已经登录
        await self.login()

        target_folder_info = await self.__yunpan_get_resource_info(target_folder)
        if target_folder_info:
            yunpan_dirs = await self.__yunpan_get_dir_info(target_folder_info.get('id'))
            if yunpan_dirs:
                for file in yunpan_dirs:
                    if file.get('name') == file_name:
                        return True
                return False

    async def yunpan_create_download_task(self, download_url: str, target_folder: str,
                                          rename: Optional[str] = None,
                                          download_same_name: bool = True,
                                          sub_file_index: Optional[List[Union[int, str]]] = None) -> Optional[bool]:
        """
        云添加：创建下载任务保存到云盘：例如下载电影，然后选择保存位置是云盘的某个路径
        注意：该功能有次数限制，使用前请查看自己是否有使用次数，非会员每天限免 3 次

        :param download_url: 资源的下载链接：磁力链接/http链接/ed2k链接等，也可以传入一个BT文件的绝对路径，例如：/Users/xxx/Downloads/xxx.torrent
        :param target_folder: 需要保存到云盘的哪个目标（例如：我的转存/电影）
        :param rename: 注意：当下载的链接是一个多文件资源，只会修改文件夹名称，如需对文件夹内文件重命名，请自行调用 yunpan_rename 方法完成。
        :param download_same_name: 当遇到同名文件或文件夹时是否继续下载，继续下载会自动在文件名后面添加 "(1)"、"(2)" 等后缀。如果跳过返回None
        :param sub_file_index: 子文件索引，默认为 None，表示下载链接包含的所有文件，当链接包含多个文件的时候，可以设置需要下载的文件序号（从1开始）['1', '2'...]
        :return:
        """
        try:
            # 判断是否已经登录
            await self.login()
            self.log.debug(f'正在创建云盘下载任务：{download_url}，保存路径：{target_folder}')

            # 判断是否是BT文件
            if download_url.endswith(".torrent"):
                download_url, _ = await self.parse_torrent(download_url)

            target_folder_info = await self.__yunpan_get_resource_info(target_folder)
            if not target_folder_info:
                self.log.error(f'无法获取 {target_folder} 的信息，请确保目标文件夹存在！')
                return False

            download_url_info = await self.get_download_url_info(download_url)
            if not download_url_info:
                self.log.error(f'无法获取下载链接信息：{download_url}')
                return False

            file_count = int(download_url_info.get('file_count', 0))

            if not download_same_name:
                if file_count > 1:
                    rename = rename or download_url_info.get('task_name')
                else:
                    rename = rename or download_url_info.get('files', [])[0].get('name')

                if await self.yunpan_file_in_folder(rename, target_folder):
                    self.log.warn(f'{rename} 已存在，跳过：{download_url}')
                    return None

            if file_count > 1:
                if sub_file_index is None:
                    sub_file_index = await self.generate_number_string_list(file_count)
                else:
                    sub_file_index = [str(int(i) - 1) for i in sub_file_index]
            else:
                sub_file_index = ["0"]

            data = {
                "upload_type": "UPLOAD_TYPE_URL",
                "kind": "drive#file",
                "parent_id": target_folder_info.get('id'),
                "name": rename,
                "url": {
                    "url": download_url,
                    "files": sub_file_index
                }
            }

            response = await self.fetch_login_after(url="https://api-pan.xunlei.com/drive/v1/files", data=data,
                                                    return_response=True)
            json_data = response.json()

            if response.status_code == 200:
                self.log.info(f'云添加任务：{download_url} 下载到云盘 {target_folder} 创建成功！')
                if rename and file_count < 2:  # 单文件重命名，多文件目录通过前面的创建请求就直接实现了文件夹的重命名
                    files = download_url_info.get('files')
                    if files:
                        file = os.path.join(target_folder, files[0].get('name'))
                    else:
                        file = os.path.join(target_folder, download_url_info.get('task_name'))

                    # 重命名称：这里需要等待云添加任务完成才行
                    for _ in range(60):  # 循环等待5分钟云添加完成
                        await asyncio.sleep(5)  # 等待5秒
                        if await self.yunpan_file_or_folder_exists(file):
                            await self.yunpan_rename(file, rename)
                            break
                        self.log.debug(
                            f'等待云添加 {download_url} 到 {target_folder} 的任务完成，已等待 {(_ + 1) * 5} 秒...')
            else:
                self.log.error(
                    f'云添加任务：{download_url} 下载到云盘 {target_folder} 创建失败：{json_data.get("error_description")}')

            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            self.log.error(f'云添加任务：{download_url} 下载到云盘 {target_folder} 创建失败：{e}')
            return False

    async def __get_file_hash(self, file_path: str = None, file_content: str = None) -> str:
        """
        计算文件的 sha1 哈希值

        :param file_path: 文件路径
        :param file_content: 文件内容（字符串格式）
        :return: 文件的 MD5 哈希值
        """
        if file_path is None and file_content is None:
            raise ValueError("必须提供文件路径或文件内容之一")

        hash_md5 = hashlib.sha1()

        if file_path:
            async with aiofiles.open(file_path, 'rb') as f:
                while True:
                    chunk = await f.read(4096)  # 逐块读取文件
                    if not chunk:
                        break
                    hash_md5.update(chunk)
        elif file_content:
            if isinstance(file_content, str):
                file_content = file_content.encode('utf-8')  # 将字符串转换为二进制格式
            hash_md5.update(file_content)

        hash_data = hash_md5.hexdigest()
        self.log.debug(f'{file_path}/{file_content} 的 MD5 哈希值：{hash_data}')
        return hash_data

    async def __get_file_info(self, file_path: str) -> Optional[Dict]:
        """
        获取文件的信息，用于创建上传任务

        :param file_path: 文件路径
        :return:
        """
        path = Path(file_path)

        if path.is_file():  # 检查路径是否为文件
            file_size = path.stat().st_size  # 获取文件大小（字节）
            file_name = path.name  # 获取文件名（包含扩展名）

            file_info = {
                "file_name": file_name,
                "file_size": file_size,
                "hash": await self.__get_file_hash(file_path)
            }
            self.log.debug(f'获取到 {file_path} 文件信息: {file_info}')
            return file_info
        else:
            self.log.error(f'路径 {file_path} 不是一个文件！')
            return None

    async def __get_upload_file_params(self, file_path: str, yunpan_save_path: str) -> Optional[Dict]:
        """
        从服务器上获取上传文件相关的API参数

        :param file_path: 本地需要上传的文件绝对路径
        :param yunpan_save_path: 云盘保存的目标文件夹路径
        :return:
        """
        self.log.debug(f'获取上传文件 {file_path} 到云盘 {yunpan_save_path} 需要的接口参数...')

        file_info = await self.__get_file_info(file_path)
        path_info = await self.__yunpan_get_resource_info(yunpan_save_path)

        if file_info and path_info:
            file_size = int(file_info.get('file_size'))

            data = {
                "kind": "drive#file",  # 文件夹类型:path_info.get('kind')
                "parent_id": path_info.get('id'),  # 目标文件夹的id
                "name": file_info.get('file_name'),
                "size": file_size,
                "space": "",
                "hash": file_info.get('hash'),  # 文件hash，一定要这个hash值，否则请求会报错，一定要这个hash值，否则请求会报错，一定要这个hash值，否则请求会报错
            }
            if file_size == 0:
                self.log.error(f'文件 {file_path} 大小为0，无法上传空文件')
                return None
            elif file_size > 1048576:  # 大于1MB
                data["upload_type"] = "UPLOAD_TYPE_RESUMABLE"  # 上传类型：UPLOAD_TYPE_FORM
            else:
                data["upload_type"] = "UPLOAD_TYPE_FORM"

            response = await self.fetch_login_after(url="https://api-pan.xunlei.com/drive/v1/files", data=data,
                                                    return_response=True)
            json_data = response.json()

            if response.status_code == 200:
                self.log.debug(f'获取上传 {file_path} 到云盘 {yunpan_save_path} 的参数：{json_data}')
                return json_data
            else:
                self.log.error(
                    f'获取上传 {file_path} 到云盘 {yunpan_save_path} 的参数失败：{json_data.get("error_description")}')
        return None

    @staticmethod
    async def __get_compute_signature_sha1(secret_access_key: str, data_to_sign: str) -> str:
        """
        计算 HMAC-SHA1 签名并返回 Base64 编码的签名
        aliyun-oss-sdk-6.7.0.min.js:computeSignature
        y.createHash("md5").update(n.from(t.content, "utf8")).digest("base64")
        createHmac("sha1", t).update(from(r, "utf8")).digest("base64")

        :param secret_access_key: 阿里云的 Access Key Secret
        :param data_to_sign: 要签名的字符串
        :return: Base64 编码的签名
        """
        signature = hmac.new(secret_access_key.encode('utf-8'),
                             data_to_sign.encode('utf-8'),
                             hashlib.sha1).digest()
        return base64.b64encode(signature).decode('utf-8')

    @staticmethod
    async def __get_compute_content_md5(content: str) -> str:
        """
        计算 MD5 哈希并返回 Base64 编码的哈希值

        :param content: 上传文件完成后包含所有ETag的XML文件结构
        :return:
        """
        # 计算 MD5 哈希
        md5_hash = hashlib.md5(content.encode('utf-8')).digest()
        # 将 MD5 哈希转换为 base64 编码
        content_md5 = base64.b64encode(md5_hash).decode('utf-8')
        return content_md5

    @staticmethod
    async def __get_oss_data() -> str:
        """
        获取阿里云 OSS 上传文件需要的参数: 时间
        :return:
        """
        # 获取当前UTC时间
        return datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    async def __parse_upload_params(self, file_path: str, yunpan_save_path: str) -> Optional[Dict]:
        """
        整理api获取上传文件需要用到的参数

        :param file_path: 本地需要上传的文件绝对路径
        :param yunpan_save_path: 云盘保存的目标文件夹路径
        :return:
        """
        await self.login()

        self.log.debug(f'整理上传文件 {file_path} 到云盘 {yunpan_save_path} 需要的参数 ...')
        # 获取上传文件的 API 信息
        upload_api = await self.__get_upload_file_params(file_path, yunpan_save_path)

        if not upload_api:
            return None

        api_params = upload_api.get('resumable', {}).get('params', {})  # 上传参数
        access_key_id = api_params.get('access_key_id')  # STS.NTEtVgZEmwmd3u7NDasD84XdL
        access_key_secret = api_params.get('access_key_secret')  # B3AFgpjbQJzPJaXgVxHTdbAr9xKF9VN7XuNK96wt8dtY
        security_token = api_params.get('security_token')  # CAISnwR1q...
        host = api_params.get('bucket') + "." + api_params.get('endpoint')  # vip-lixian-08.up.xdrive.xunlei.com
        # 上传文件的接口：https://vip-lixian-08.up.xdrive.xunlei.com/upload_tmp/07DC450F3F974022EBFE917E8AE2AC5488314BEF_1728716014690270273
        upload_url = "https://" + host + '/' + api_params.get('key')

        # /vip-lixian-08/upload_tmp/07DC450F3F974022EBFE917E8AE2AC5488314BEF_1728716014690270273
        request_path = f"{'/' + api_params.get('bucket') + '/' + api_params.get('key')}"

        api_file = upload_api.get('file', {})  # 文件信息
        content_type = api_file.get('file_category') + '/' + api_file.get('file_extension').strip('.')  # 文件类型
        content_type = content_type.lower()  # 转换为小写
        file_name = api_file.get('file_name')
        file_size = api_file.get('file_size')

        oss_user_agent = 'aliyun-sdk-js/6.7.0 Chrome 129.0.0.0 on Windows 10 64-bit'

        oss_date = await self.__get_oss_data()

        upload_id_sign = (
            f"POST\n"
            f"\n"  # content_md5为空
            f"{content_type}\n"
            f"{oss_date}\n"
            f"x-oss-date:{oss_date}\n"
            f"x-oss-security-token:{security_token}\n"
            f"x-oss-user-agent:{oss_user_agent}\n"
            f"{request_path + '?uploads'}"
        )

        # 生成 base64 编码的签名
        compute_signature = await self.__get_compute_signature_sha1(access_key_secret, upload_id_sign)

        authorization_front = f"OSS {api_params.get('access_key_id')}:"  # OSS 前部分，需要补上签名

        headers = {
            "Content-Type": content_type,
            "authorization": authorization_front + compute_signature,
            "x-oss-date": oss_date,
            "x-oss-security-token": security_token,
            "x-oss-user-agent": "aliyun-sdk-js/6.7.0 Chrome 129.0.0.0 on Windows 10 64-bit"
        }
        xml_data = await self.get_response(url=upload_url, params={"uploads": ""}, return_json=False,
                                           headers=headers, post=True)
        if not xml_data:
            self.log.error('获取获取UploadId失败！')
            return
        # 使用正则表达式提取 UploadId
        match = re.search(r'<UploadId>(.*?)</UploadId>', xml_data)

        if match:
            upload_id = match.group(1)
            self.log.debug(f'获取UploadId: {upload_id}')

            upload_params = {
                '__upload_large_file': upload_url,
                'host': host,
                'upload_id': upload_id,
                'access_key_id': access_key_id,
                'access_key_secret': access_key_secret,
                'security_token': security_token,
                'authorization_front': authorization_front,
                'oss_user_agent': oss_user_agent,
                'request_path': request_path,
                'file_name': file_name,
                'file_size': file_size
            }

            return upload_params
        else:
            self.log.error('获取获取UploadId失败！')
            return None

    async def __get_part_signature(self, upload_params: Dict, part_number: Union[int, str], oss_date: str):
        """
        获取分片上传的签名

        :param upload_params: 上传的参数
        :param part_number: 分片编号
        :param oss_date: 阿里云 OSS 上传文件需要的时间
        :return:
        """

        sign = (
            f"PUT\n"
            f"\n"
            f"application/octet-stream\n"
            f"{oss_date}\n"
            f"x-oss-date:{oss_date}\n"
            f"x-oss-security-token:{upload_params.get('security_token')}\n"
            f"x-oss-user-agent:{upload_params.get('oss_user_agent')}\n"
            f"{upload_params.get('request_path') + '?partNumber=' + str(part_number) + '&uploadId=' + upload_params.get('upload_id')}"
        )

        return await self.__get_compute_signature_sha1(upload_params.get('access_key_secret'), sign)

    async def __upload_file_parts(self, upload_params: Dict, part_number: Union[int, str],
                                  put_data: str, content_length: Union[int, str]) -> Optional[Dict]:
        """
        上传分片

        :param upload_params: 上传的参数
        :param part_number: 分片编号
        :param put_data: 上传的数据
        :param content_length: 数据长度
        :return:
        """

        params = {
            "partNumber": str(part_number),
            "uploadId": upload_params.get('upload_id')
        }
        oss_date = await self.__get_oss_data()
        authorization = (upload_params.get('authorization_front') +
                         await self.__get_part_signature(upload_params, part_number, oss_date))

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Length": str(content_length),
            "Content-Type": "application/octet-stream",
            "Host": upload_params.get('host'),  # "vip-lixian-04.up.xdrive.xunlei.com"
            "Origin": "https://pan.xunlei.com",
            "Pragma": "no-cache",
            "Referer": "https://pan.xunlei.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "authorization": authorization,  # "OSS STS.NV5QC3PPNkpwqRaePzC1msfZD:ExWg9E8/CvMjxECTOCh9ozcMvXQ=",
            "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "x-oss-date": oss_date,  # "Sat, 12 Oct 2024 05:57:16 GMT",
            "x-oss-security-token": upload_params.get('security_token'),
            "x-oss-user-agent": upload_params.get('oss_user_agent')
        }
        try:
            self.log.debug(f"上传分片: {part_number}")
            async with httpx.AsyncClient() as client:
                response = await client.put(upload_params.get('__upload_large_file'), params=params,
                                            headers=headers,
                                            data=put_data)  # 1MB的空字节内容
                if response.status_code == 200:
                    self.log.debug(f"上传分片成功: {part_number}")
                    etag = response.headers.get('etag').strip('"')
                    return {
                        'part_number': part_number,
                        'etag': etag
                    }
        except Exception as e:
            self.log.error(f"上传分片失败: {e}")
            return None

    async def __get_complete_signature(self, upload_params: Dict, content_md5: str, oss_date: str):
        """
        获取分片上传的签名

        :param upload_params: 上传的参数
        :param content_md5: 文件的MD5值
        :param oss_date: 阿里云 OSS 上传文件需要的时间
        :return:
        """
        sign = (
            f"POST\n"
            f"{content_md5}\n"  # content_md5为空
            f"application/xml\n"
            f"{oss_date}\n"
            f"x-oss-date:{oss_date}\n"
            f"x-oss-security-token:{upload_params.get('security_token')}\n"
            f"x-oss-user-agent:{upload_params.get('oss_user_agent')}\n"
            f"{upload_params.get('request_path') + '?uploadId=' + upload_params.get('upload_id')}"
        )
        return await self.__get_compute_signature_sha1(upload_params.get('access_key_secret'), sign)

    @staticmethod
    def __construct_xml(etags: List) -> str:
        """
        构造 XML 数据

        :param etags: ETag列表
        :return: XML数据
        """
        parts_xml = '\n'.join([f'''<Part>
<PartNumber>{etag.get('part_number')}</PartNumber>
<ETag>"{etag.get('etag')}"</ETag>
</Part>''' for etag in etags])
        complete_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<CompleteMultipartUpload>
{parts_xml}
</CompleteMultipartUpload>"""
        return complete_xml

    async def __upload_file_xml(self, upload_params: Dict, etags: Dict) -> bool:
        """
        完成上传：发送xml分片结构信息到服务器完成上传

        :param upload_params: 上传的参数
        :param etags: 包含所有分片的ETag信息
        :return:
        """

        complete_xml = self.__construct_xml(etags)

        params = {
            "uploadId": upload_params.get('upload_id')
        }
        oss_date = await self.__get_oss_data()

        content_md5 = await self.__get_compute_content_md5(complete_xml)
        authorization = (upload_params.get('authorization_front') +
                         await self.__get_complete_signature(upload_params, content_md5, oss_date))

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Length": str(len(complete_xml)),
            "Content-Md5": content_md5,
            "Content-Type": "application/xml",
            "Host": upload_params.get('host'),  # "vip-lixian-04.up.xdrive.xunlei.com",
            "Origin": "https://pan.xunlei.com",
            "Pragma": "no-cache",
            "Referer": "https://pan.xunlei.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "authorization": authorization,
            "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "x-oss-date": oss_date,  # "Sat, 12 Oct 2024 09:47:15 GMT",
            "x-oss-security-token": upload_params.get('security_token'),
            "x-oss-user-agent": upload_params.get('oss_user_agent')
        }
        try:
            async with httpx.AsyncClient() as client:
                r = await client.post(url=upload_params.get('__upload_large_file'), headers=headers, params=params,
                                      data=complete_xml)
                if r.status_code == 200:
                    self.log.debug(f"完成上传: {upload_params.get('file_name')}")
                    return True
        except Exception as e:
            self.log.error(f"上传xml结构数据失败: {e}")
            return False

    async def __upload_large_file(self, file_path: str, yunpan_save_path: str, max_concurrency: int = 5) -> bool:
        """
        上传大于1M的文件到迅雷云盘

        :param file_path: 本地文件的绝对路径
        :param yunpan_save_path: 云盘保存的目标文件夹路径："我的转存/电影"
        :param max_concurrency: 最大并发数，默认为5，最大为10
        :return:
        """
        max_concurrency = min(max_concurrency, 10)
        upload_params = await self.__parse_upload_params(file_path, yunpan_save_path)

        file_size = int(os.path.getsize(file_path))

        part_size = 1048576  # 1MB
        num_parts = (file_size + part_size - 1) // part_size  # 计算需要的部分数

        tasks = []
        semaphore = asyncio.Semaphore(max_concurrency)  # 设置最大并发量为10

        async def upload_part(part_number: int):
            async with semaphore:  # 限制并发
                with open(file_path, 'rb') as f:
                    f.seek((part_number - 1) * part_size)  # 定位到当前分片的位置
                    part_data = f.read(part_size)  # 读取分片数据
                    content_length = len(part_data)
                    return await self.__upload_file_parts(upload_params, part_number, part_data, content_length)

        # 创建任务
        for part_number in range(1, num_parts + 1):
            tasks.append(upload_part(part_number))

        etags = await asyncio.gather(*tasks)

        if not etags:
            return False

        # 发送xml文件结构请求完成上传
        return await self.__upload_file_xml(upload_params, etags)

    async def yunpan_create_link_file_api(self, link_name: str, link_url: str, yunpan_save_path: str):
        """
        迅雷云盘新建链接文件

        :param link_name: 链接名称
        :param link_url: 链接地址
        :param yunpan_save_path: 云盘保存的目标文件夹路径
        :return:
        """
        await self.login()

        # 创建Internet Shortcut文件的内容
        shortcut_content = f"[InternetShortcut]\nURL={link_url}"

        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            # 在临时目录中创建指定名称的文件
            filepath = os.path.join(temp_dir, f"{link_name.strip('.url')}.url")

            # 使用aiofiles进行异步文件写入
            async with aiofiles.open(filepath, 'w', encoding='utf-8') as temp_file:
                await temp_file.write(shortcut_content)

            # 上传文件
            return await self.yunpan_upload_file(filepath, yunpan_save_path)

    async def __yunpan_get_share_link_params(self, share_id: str, pwd: str = None) -> Optional[Dict]:
        """
        获取迅雷云盘分享链接转存需要用到的参数

        :param share_id: 分享链接中的分享ID
        :param pwd: 提取码
        :return:
        """
        params = {
            "share_id": share_id,
            "pass_code": pwd,
            "limit": "100",
            "pass_code_token": "",
            "page_token": "",
            "thumbnail_size": "SIZE_SMALL"
        }

        json_data = await self.fetch_login_after(url="https://api-pan.xunlei.com/drive/v1/share", params=params)

        if json_data and json_data.get('share_status') == 'OK':
            sharer_nickname = json_data.get('user_info', {}).get('nickname')  # 分享者昵称
            sharer_id = json_data.get('user_info', {}).get('nickname')  # 分享者昵称
            files = json_data.get('files', [])
            share_root = files[0]  # 分享链接的文件/根目录
            kind = share_root.get('kind')
            if kind == 'drive#file':
                size = share_root.get('size')
                count = 1
            elif kind == 'drive#folder':  # 文件夹
                size = share_root.get('params', {}).get('file_property_size')  # 文件夹大小
                count = int(share_root.get('params', {}).get('file_property_count', 0))  # 文件夹文件数量，0表示空文件夹
            else:
                size = None
                count = None

            return {
                "title": json_data.get('title'),
                "pass_code_token": json_data.get('pass_code_token'),
                "next_page_token": json_data.get('next_page_token'),
                "kind": share_root.get('kind'),
                "id": share_root.get('id'),
                "parent_id": share_root.get('parent_id'),
                "name": share_root.get('name'),
                "size": size,
                "count": count,
                "hash": share_root.get('hash'),
                "sharer_nickname": sharer_nickname,
                "sharer_id": sharer_id,
            }
        elif json_data.get('share_status') == 'PASS_CODE_ERROR':
            self.log.error(f"提取码错误，请检查提取码 {pwd} 是否正确！")
            return None
        else:
            self.log.error(f"解析分享链接 {share_id} 失败：{json_data.get('share_status_text', json_data)}")
            return None

    async def yunpan_get_space_info(self, return_raw_data: bool = False) -> Optional[Dict]:
        """
        获取迅雷用户云盘空间容量情况

        :param return_raw_data: 返回原始数据
        :return:
        """
        await self.login()

        json_data = await self.fetch_login_after(url="https://api-pan.xunlei.com/drive/v1/about")
        if json_data:
            if return_raw_data:
                return json_data
            try:
                quota = json_data.get('quota', {})
                limit = int(quota.get('limit', 0))  # 容量单位 字节
                usage = int(quota.get('usage', 0))  # 已使用单位 字节
                usage_in_trash = int(quota.get('usage_in_trash', 0))  # 回收站使用单位 字节

                self.log.info(
                    f'迅雷用户云盘空间大小上限为：{round(limit / (1024 ** 3), 2)} GB，已使用：{round(usage / (1024 ** 3), 2)} GB，回收站使用：{round(usage_in_trash / (1024 ** 3), 2)} GB')
                return {'limit': limit, 'usage': usage, 'usage_in_trash': usage_in_trash,
                        'free_space': (limit - usage - usage_in_trash)}
            except Exception as e:
                self.log.error(f'提取迅雷用户云盘空间大小上限失败：{e}')
                return None
        else:
            self.log.error("获取迅雷用户云盘空间大小上限失败！")
            return None

    async def yunpan_get_create_offline_task_limit(self) -> Optional[Dict]:
        """获取迅雷用户云盘离线下载次数上限"""
        await self.login()
        params = {
            "space": "",
            "with_quotas": "CREATE_OFFLINE_TASK_LIMIT"
        }

        json_data = await self.fetch_login_after(
            url="https://api-pan.xunlei.com/drive/v1/about", params=params)
        if json_data:
            try:
                task_limit = json_data.get('quotas', {}).get('CREATE_OFFLINE_TASK_LIMIT', {})

                self.log.info(f'迅雷用户云盘离线下载/云添加任务次数上限为：{task_limit} 次')
                return {
                    "limit": int(task_limit.get('limit')),  # 上限
                    "usage": int(task_limit.get('usage')),  # 已使用
                    "remain": int(task_limit.get('limit')) - int(task_limit.get('usage'))  # 剩余次数

                }
            except Exception as e:
                self.log.error(f'提取迅雷用户云盘离线下载/云添加任务次数上限失败：{e}')
                return None
        else:
            self.log.error("获取迅雷用户云盘离线下载/云添加任务次数上限失败！")
            return None

    async def yunpan_upload_file(self, file_path: str, yunpan_save_path: str, retry_times: int = 1,
                                 max_concurrency: int = 5) -> bool:
        """
        上传文件到云盘
        注意：普通用户每天有 1G 的文件上传限额

        :param file_path: 本地需要上传的文件绝对路径
        :param yunpan_save_path: 云盘保存的目标文件夹路径
        :param retry_times: 上传失败后重试的次数
        :param max_concurrency: 并发上传文件数量，默认为 5，需小于等于10
        :return: 上传是否成功
        """
        await self.login()

        # 获取上传文件的 API 信息
        upload_params = await self.__get_upload_file_params(file_path, yunpan_save_path)

        if not upload_params:
            return False
        self.log.info(f'上传 {file_path} 到云盘 {yunpan_save_path} ...')

        # 重试逻辑
        for attempt in range(retry_times + 1):  # +1 是因为我们需要尝试一次加上重试次数
            try:
                if upload_params.get('upload_type') == 'UPLOAD_TYPE_FORM':  # 小文件
                    # 解析上传参数
                    form = upload_params.get('form', {})
                    upload_url = form.get('url')
                    multi_parts = form.get('multi_parts')

                    # 上传文件
                    async with httpx.AsyncClient() as client:
                        with open(file_path, 'rb') as f:
                            files = {
                                'OSSAccessKeyId': (None, multi_parts['OSSAccessKeyId']),
                                'Signature': (None, multi_parts['Signature']),
                                'callback': (None, ''),
                                'key': (None, multi_parts['key']),
                                'policy': (None, multi_parts['policy']),
                                'x:user_data': (None, multi_parts['x:user_data']),
                                'file': (file_path.split('/')[-1], f, 'text/plain'),
                            }
                            r = await client.post(upload_url, files=files)

                            if r.status_code // 100 == 2:  # 2xx
                                self.log.info(f"上传文件 {file_path} 到 {yunpan_save_path} 已完成")
                                return True  # 成功上传，返回 True

                else:
                    if await self.__upload_large_file(file_path, yunpan_save_path, max_concurrency=max_concurrency):
                        return True

            except Exception as e:
                self.log.error(f"上传文件 {file_path} 失败: {e}")

            # 如果上传失败且还有重试次数，则记录信息并等待
            if attempt < retry_times:
                self.log.info(f"上传失败！第 {attempt + 1} 次重试上传文件 {file_path} 到 {yunpan_save_path} ...")

        return False  # 所有重试均失败

    async def yunpan_upload_folder(self, local_folder_path: str, yunpan_save_path: str,
                                   concurrent_limit: int = 3, retry_times: int = 1) -> None:
        """
        上传文件夹到云盘

        :param local_folder_path: 本地需要上传的文件夹绝对路径
        :param yunpan_save_path: 云盘保存的目标文件夹路径
        :param concurrent_limit: 并发上传文件数量，必须大于0，官方限制且不能超过5，默认为3
        :param retry_times: 上传失败后重试的次数
        :return:
        """
        if concurrent_limit < 1 or concurrent_limit > 5:
            raise ValueError("concurrent_limit 参数取值不能小于1或大于5")

        start_time = time.time()
        await self.login()
        self.log.info(f'上传文件夹 {local_folder_path} 到云盘 {yunpan_save_path}，并发上限为：{concurrent_limit} ...')

        root_dir = os.path.basename(local_folder_path)  # 获取根目录名称

        # 创建根目录
        folder_info = await self.__yunpan_create_folder(root_dir, yunpan_save_path)
        if not folder_info:
            return

        # 当前云盘根目录信息
        current_yp_folder = yunpan_save_path + '/' + os.path.basename(local_folder_path)

        # 创建信号量
        semaphore = asyncio.Semaphore(concurrent_limit)

        async def create_folder_with_limit(folder_name, new_folder):
            async with semaphore:
                return await self.__yunpan_create_folder(folder_name, new_folder)

        async def upload_file_with_limit(file_path, new_folder):
            async with semaphore:
                return await self.yunpan_upload_file(file_path, new_folder, retry_times)

        create_folders_tasks = []  # 创建文件夹任务
        upload_tasks = []  # 上传文件任务

        for root, folders, files in os.walk(local_folder_path):
            # 计算相对路径并构建新目录路径
            relative_path = os.path.relpath(root, local_folder_path)
            new_folder = os.path.join(current_yp_folder, relative_path) if relative_path != '.' else current_yp_folder

            # 创建目录
            for f in folders:
                # 创建文件夹
                create_folders_tasks.append(create_folder_with_limit(f, new_folder))

            # 上传文件
            for f in files:
                local_file_path = os.path.join(root, f)
                upload_tasks.append(upload_file_with_limit(local_file_path, new_folder))

        # 使用并发，先创建文件夹再上传文件
        create_folder_results = await asyncio.gather(*create_folders_tasks)
        upload_file_results = await asyncio.gather(*upload_tasks)

        # 统计创建文件夹和上传文件的结果
        success_create_folders = 0  # 记录成功创建文件夹的数量
        failed_create_folders = 0  # 记录失败创建文件夹的数量
        success_upload_files = 0  # 记录成功上传文件的数量
        failed_upload_files = 0  # 记录失败上传文件的数量
        for result in create_folder_results:
            if result:  # 假设返回True表示成功
                success_create_folders += 1
            else:
                failed_create_folders += 1

        for result in upload_file_results:
            if result:  # 假设返回True表示成功
                success_upload_files += 1
            else:
                failed_upload_files += 1

        self.log.info(
            f"上传文件夹 {local_folder_path} 到云盘 {yunpan_save_path} 已完成，耗时：{round(time.time() - start_time, 2)} 秒。"
            f" 创建文件夹成功：{success_create_folders}，失败：{failed_create_folders}。"
            f" 上传文件成功：{success_upload_files}，失败：{failed_upload_files}。"
        )

    async def yunpan_upload_task(self, local_path: str, yunpan_save_path: str, concurrent_limit: int = 3):
        """
        上传文件到云盘，支持文件、文件夹

        :param local_path: 本地文件或文件夹绝对路径
        :param yunpan_save_path: 云盘保存的目标文件夹路径
        :param concurrent_limit: 文件夹上传时的并发上传文件数量，必须大于0，官方限制且不能超过5，，默认为3
        :return:
        """
        if os.path.isdir(local_path):
            await self.yunpan_upload_folder(local_path, yunpan_save_path, concurrent_limit)
        else:
            await self.yunpan_upload_file(local_path, yunpan_save_path)

    async def __yunpan_get_share_link_details(self, share_id: str, parent_id: str, pass_code_token: str,
                                              current_folder_path: str = '') -> Optional[List[Dict]]:
        """
        获取迅雷云盘分享链接文件夹里面的文件详情

        :param share_id: 分享链接中提取的 share_id
        :param parent_id: 分享链接中提取的根目录或当前目录的 id
        :param pass_code_token: 提取码 token
        :param current_folder_path: 当前目录路径
        :return:
        """
        self.log.debug(f"正在获取分享链接目录： {current_folder_path} 中的文件详情...")
        file_list = []  # 用于存储文件详情的列表
        next_page_token = ""  # 初始化 next_page_token

        while True:
            params = {
                "share_id": share_id,
                "parent_id": parent_id,
                "pass_code_token": pass_code_token,
                "limit": "100",
                "page_token": next_page_token,
                "thumbnail_size": "SIZE_SMALL"
            }

            json_data = await self.fetch_login_after(url="https://api-pan.xunlei.com/drive/v1/share/detail",
                                                     params=params)
            if json_data and json_data.get('share_status') == 'OK':
                files = json_data.get('files', [])
                for file in files:
                    kind = file.get('kind')
                    file_id = file.get('id')
                    file_name = file.get('name')
                    file_path = os.path.join(current_folder_path, file_name)

                    if kind == 'drive#file':
                        size = file.get('size')
                        count = 1
                    elif kind == 'drive#folder':  # 文件夹
                        size = file.get('params', {}).get('file_property_size')  # 文件夹大小
                        count = int(file.get('params', {}).get('file_property_count', 0))  # 文件夹文件数量，0表示空文件
                    else:
                        size = None
                        count = None

                    file_list.append({
                        "next_page_token": json_data.get('next_page_token'),
                        "kind": file.get('kind'),
                        "real_path": file_path,
                        "parent_path": current_folder_path,
                        "id": file_id,
                        # "parent_id": file.get('parent_id'),  # 父文件夹id，用不到
                        "name": file_name,
                        "size": size,
                        "count": count,
                        "hash": file.get('hash'),
                    })

                    # 递归获取子文件夹内容
                    if kind == 'drive#folder' and count > 0:
                        child_files = await self.__yunpan_get_share_link_details(
                            share_id, file_id, pass_code_token, file_path
                        )
                        if child_files:
                            file_list.extend(child_files)

                # 更新 next_page_token，检查是否还有更多页面
                next_page_token = json_data.get('next_page_token')
                if not next_page_token:  # 如果没有下一页，则退出循环
                    break
            else:
                self.log.error(f"获取 {share_id} 文件夹内部内容失败：{json_data}")
                return None
        self.log.debug(f"获取 {share_id} 文件夹内部内容: {file_list}")
        return file_list

    async def yunpan_get_all_share_link(self, return_raw_data: bool = False, only_useful: bool = False,
                                        save_path: str = None) -> Optional[List[Dict]]:
        """
        获取迅雷云盘所有的分享链接

        :param return_raw_data: 是否返回原始数据
        :param only_useful: 只返回有效分享链接，默认为False，返回所有分享链接
        :param save_path: 迅雷云盘分享数据文件要存放的文件夹路径/文件，默认为None，不保存。
        :return:
        """
        share_links = []
        next_page_token: str = ''

        while True:
            params = {
                "space": "",
                "limit": "100",
                "withCaptcha": "true",
                "withCredentials": "true",
                "page_token": next_page_token  # 使用传入的 token
            }

            json_data = await self.fetch_login_after(url="https://api-pan.xunlei.com/drive/v1/share/list",
                                                     params=params)

            if not json_data:
                self.log.error("获取分享链接列表失败")
                return None

            links_data = json_data.get('data', [])
            if only_useful:
                links_data = [item for item in links_data if item.get('share_status') == 'OK']

            # 整理数据
            if return_raw_data:
                share_links.extend(links_data)
            else:
                for item in links_data:
                    share_links.append({
                        "share_status": item.get('share_status'),  # 分享状态
                        "title": item.get('title'),
                        "share_url": item.get('share_url'),
                        "pass_code": item.get('pass_code'),
                        "file_num": item.get('file_num'),
                        "restore_count": item.get('restore_count'),
                        "expiration_left_seconds": item.get('expiration_left_seconds'),
                        "view_count": item.get('view_count'),
                        "uploader": item.get('XiaoqiangClub'),
                        "uploader_id": item.get('user_id'),
                        "share_id": item.get('share_id'),
                        "file_id": item.get('file_id'),
                        "kind": item.get('file_kind'),
                        "file_size": item.get('file_size'),
                    })

            # 获取下一页的 token
            next_page_token = json_data.get('next_page_token')

            # 如果没有下一页，退出循环
            if not next_page_token:
                break

        self.log.info(f"共获取到 {len(share_links)} 个分享链接")
        if save_path:
            # 判断save_path是不是一个文件夹
            if os.path.isdir(save_path):
                save_file = os.path.join(save_path, f"xunlei_yunpan_share_links_{time.strftime('%Y%m%d%H%M%S')}.json")
            else:
                save_file = save_path

            # 异步方式将share_links数据保存到文件
            async with aiofiles.open(save_file, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(share_links, ensure_ascii=False, indent=4))

        return share_links

    async def yunpan_share_link_transfer(self, share_link: str, yunpan_save_path: str,
                                         transfer_name_list: List[str] = None, exact_match: bool = True,
                                         keep_directory_structure: bool = True,
                                         use_all_space_when_insufficient: bool = False,
                                         every_times_transfer_num: int = 300, match_depth: int = -1,
                                         pwd: str = None) -> bool:
        """
        迅雷分享链接资源转存，支持关键字模糊转存，详情看参数说明

        :param share_link: 分享链接，可直接将密码包含其中：https://pan.xunlei.com/s/VO95N0dq343nbWV_t0WtvqpMA1?pwd=wyyh
        :param yunpan_save_path: 需要保存到云盘目录的路径
        :param transfer_name_list: 需要转存的文件/文件夹列表，只匹配根目录的文件/文件夹，如果需要保存包含指定关键字的资源，需要将exact_match参数设置为False，如果设置了该参数，则只保存该列表中的文件，默认为None，转存全部文件
        :param exact_match: 是否精确匹配文件名，True：文件名要完全匹配，False：文件名只要包含即可，默认为True
        :param keep_directory_structure: 是否保留目录结构，配合transfer_name_list参数使用。True：保留目录结构False：不保留目录结构：默认为True
        :param use_all_space_when_insufficient: 当云盘空间不足时，是否逐个文件的尽量保存，知道空间用完，默认为False，不启用。
        :param every_times_transfer_num: 每次转存数量，默认为300。普通用户每次转存最多转存500个文件，自动忽略空文件夹。高级用法：当你的云盘容量不足的时，设置一个较低的数字实现尽可能多的转存。
        :param match_depth: 匹配文件/文件夹的深度，默认值为1，即只匹配根目录的文件/文件夹，设置为-1表示匹配所有深度
        :param pwd: 提取码，如果分享链接没有包含提取码就必须设置提取码参数，优先使用pwd参数的提取码
        :return:
        """
        await self.login()
        self.log.info(f'转存分享链接 {share_link} 到云盘 {yunpan_save_path} ...')

        # 检查并提取分享链接和提取码
        share_id, password = self.__extract_share_id_and_password(share_link, pwd)
        if not share_id or not password:
            self.log.error(f'请提供分享链接 {share_link} 的有效提取码')
            return False

        # 获取分享链接参数
        share_params = await self.__yunpan_get_share_link_params(share_id, password)
        if not share_params:
            return False

        # 检查云盘空间是否足够
        if not await self.__check_free_space(share_params.get('size')):
            if use_all_space_when_insufficient:
                self.log.info('云盘空间不足，将尽可能多的保存文件到云盘...')
            else:
                return False

        # 获取需要转存的文件或文件夹
        file_ids = await self.__get_file_ids_to_transfer(share_id, share_params, transfer_name_list, exact_match,
                                                         match_depth,
                                                         yunpan_save_path)
        if not file_ids:
            self.log.info(f'分享链接 {share_link} 中没有包含 transfer_name_list 设定的文件，跳过转存')
            return True

        # 转存文件或文件夹到云盘
        return await self.__transfer_files_to_yunpan(file_ids, share_id, share_params, every_times_transfer_num,
                                                     keep_directory_structure, yunpan_save_path,
                                                     use_all_space_when_insufficient)

    def __extract_share_id_and_password(self, share_link: str, pwd: str) -> (str, str):
        """提取分享链接中的 share_id 和 password"""
        self.log.debug('提取分享链接中的 share_id 和 password')
        if '?pwd=' not in share_link and not pwd:
            return None, None

        share_id = share_link.strip().split('/s/')[-1].split('?')[0]
        password = pwd if pwd else None
        if '?pwd=' in share_link and not password:
            share_link, extracted_pass_code = share_link.strip().split('?pwd=')
            password = extracted_pass_code.strip().strip('#')

        return share_id, password

    async def __check_free_space(self, required_size: int) -> bool:
        """检查云盘空间是否足够"""
        self.log.debug('检查云盘空间是否足够')
        space_info = await self.yunpan_get_space_info()
        if not space_info:
            return False
        free_space = space_info.get('free_space')
        if free_space < int(required_size):
            self.log.error('云盘剩余空间不足，无法转存，请清理云盘空间后再试！')
            return False
        return True

    async def __get_file_ids_to_transfer(self, share_id, share_params: dict, transfer_name_list: List[str],
                                         exact_match: bool, match_depth: int, yunpan_save_path: str) -> List[dict]:
        """获取需要转存的文件或文件夹的ID"""
        self.log.debug('获取需要转存的文件或文件夹的ID')
        if share_params.get('kind') == 'drive#folder':
            return await self.__get_folder_file_ids(share_id, share_params, transfer_name_list, exact_match,
                                                    match_depth, yunpan_save_path)
        else:
            return [{'parent_path': yunpan_save_path, 'id': share_params.get('id')}]

    async def __get_folder_file_ids(self, share_id: str, share_params: dict, transfer_name_list: List[str],
                                    exact_match: bool, match_depth: int, yunpan_save_path: str) -> List[dict]:
        """获取文件夹内需要转存的文件或文件夹的ID"""
        self.log.debug('获取文件夹内需要转存的文件或文件夹的ID')
        root_folder = share_params.get('title')

        if transfer_name_list:
            yunpan_save_path = os.path.join(yunpan_save_path, root_folder)
            file_ids = await self.__filter_files(share_id, share_params, exact_match,
                                                 match_depth, yunpan_save_path, transfer_name_list)
        elif share_params.get('count') > 499:  # 列表长度大于499，普通用户不支持，需要分页转存
            self.log.info('分享链接中文件数量大于 499，无法直接转存，开始分页转存...')
            yunpan_save_path = os.path.join(yunpan_save_path, root_folder)
            file_ids = await self.__filter_files(share_id, share_params, exact_match,
                                                 match_depth, yunpan_save_path)
        else:
            file_ids = [{'parent_path': yunpan_save_path, 'id': share_params.get('id')}]

        return file_ids

    async def __filter_files(self, share_id, share_params: dict,
                             exact_match: bool, match_depth: int, yunpan_save_path: str,
                             transfer_name_list: List[str] = None) -> List[dict]:
        """过滤需要转存的文件或文件夹"""
        self.log.info('开始过滤需要转存的文件或文件夹，时间耗时较长，请耐心等待...')

        share_link_all_files = await self.__yunpan_get_share_link_details(
            share_id, share_params['id'], share_params['pass_code_token'],
            yunpan_save_path)

        file_ids = []
        parent_path_set = set()
        if transfer_name_list:
            for file in share_link_all_files:
                file_name = file.get('name')
                real_path = file.get('real_path')

                if match_depth != -1:
                    depth = real_path.count(os.sep) - yunpan_save_path.count(os.sep)
                    if depth > match_depth:
                        continue

                if exact_match:
                    if file_name in transfer_name_list:
                        file_ids.append(file)
                        if file.get('kind') == 'drive#folder':
                            parent_path_set.add(file.get('real_path'))
                else:
                    if any(name in file_name for name in transfer_name_list):
                        file_ids.append(file)
                        if file.get('kind') == 'drive#folder':
                            parent_path_set.add(file.get('real_path'))

            file_ids = [file for file in file_ids if file.get('parent_path') not in parent_path_set]

        else:
            # 先将所有文件和文件夹添加到 all_files 和 all_folders 列表中
            for file in share_link_all_files:
                if file.get('kind') == 'drive#file':
                    file_ids.append(file)

        return file_ids

    async def __transfer_files_to_yunpan(self, file_ids: List[dict], share_id: str, share_params: dict,
                                         every_times_transfer_num: int, keep_directory_structure: bool,
                                         yp_save_root_path: str, use_all_space_when_insufficient: bool) -> bool:
        """将文件或文件夹转存到云盘"""
        success_count = 0
        failure_count = 0

        async def transfer_files(batch_file_ids, current_parent_id):
            nonlocal success_count, failure_count
            if await self.__batch_transfer_files(share_id, share_params, current_parent_id, batch_file_ids):
                success_count += len(batch_file_ids)
                return True
            else:
                failure_count += len(batch_file_ids)
                return False

        if keep_directory_structure:  # 保留目录结构
            self.log.info('开始转存文件，保留目录结构')
            grouped_files = await self.__group_files_by_parent_path(file_ids)
            for parent_path, files in grouped_files.items():
                current_transfer_num = every_times_transfer_num  # 重置为默认值

                current_parent_id = await self.__get_or_create_folder_id(parent_path, yp_save_root_path)
                if not current_parent_id:
                    return False

                i = 0
                while i < len(files):
                    batch_file_ids = [file['id'] for file in files[i:i + current_transfer_num]]
                    if not await transfer_files(batch_file_ids, current_parent_id):
                        if use_all_space_when_insufficient:
                            if current_transfer_num > 50:
                                current_transfer_num -= 50
                            elif current_transfer_num > 10:
                                current_transfer_num -= 10
                            elif current_transfer_num > 2:
                                current_transfer_num -= 1
                            else:
                                self.log.error('云盘空间不足，无法继续转存！')
                                return False
                            self.log.info(f'云盘空间不足，减少转存数量至 {current_transfer_num}，继续转存...')
                        else:
                            return False
                    else:
                        i += current_transfer_num
        else:  # 不保留目录结构
            current_transfer_num = every_times_transfer_num
            self.log.info('开始转存文件，不保留目录结构，将所有文件转存到根目录')
            parent_info = await self.__yunpan_get_resource_info(yp_save_root_path)

            i = 0
            while i < len(file_ids):
                batch_file_ids = [file['id'] for file in file_ids[i:i + current_transfer_num]]
                if not await transfer_files(batch_file_ids, parent_info.get('id')):
                    if use_all_space_when_insufficient:
                        if current_transfer_num > 50:
                            current_transfer_num -= 50
                        elif current_transfer_num > 10:
                            current_transfer_num -= 10
                        elif current_transfer_num > 2:
                            current_transfer_num -= 1
                        else:
                            self.log.error('云盘空间不足，无法继续转存！')
                            return False
                        self.log.info(f'云盘空间不足，减少转存数量至 {current_transfer_num}，继续转存...')
                    else:
                        return False
                else:
                    i += current_transfer_num

        self.log.info(f'转存完成！成功转存 {success_count} 个，失败转存 {failure_count} 个。')
        return True

    async def __group_files_by_parent_path(self, file_ids: List[dict]) -> dict:
        """将文件根据父路径分组"""
        self.log.debug(f'将文件根据父路径分组：{file_ids}')
        grouped_files = {}
        for file in file_ids:
            parent_path = file.get('parent_path')
            if parent_path not in grouped_files:
                grouped_files[parent_path] = []
            grouped_files[parent_path].append(file)
        return grouped_files

    async def __get_or_create_folder_id(self, parent_path: str, yp_save_root_path: str) -> Optional[str]:
        """获取或创建文件夹ID，逐级检查从yp_save_root_path到parent_path，没有就自动新建"""
        # 首先尝试获取目标文件夹的信息
        folder_info = await self.__yunpan_get_resource_info(parent_path)

        if folder_info:
            return folder_info.get('id')

        self.log.info(f'目标文件夹 {parent_path} 不存在，开始逐级检查并创建...')

        # 如果目标文件夹不存在，则开始逐级检查和创建
        path_parts = os.path.relpath(parent_path, yp_save_root_path).split(os.sep)
        current_path = yp_save_root_path

        for part in path_parts:
            current_path = os.path.join(current_path, part)
            folder_info = await self.__yunpan_get_resource_info(current_path)
            if not folder_info:
                folder_info = await self.__yunpan_create_folder(part, os.path.dirname(current_path))
                if not folder_info:
                    self.log.error(f"Failed to create folder: {current_path}")
                    return None
        return folder_info.get('id')

    async def __batch_transfer_files(self, share_id: str, share_params: dict, parent_id: str,
                                     file_ids: List[str]) -> bool:
        """批量转存文件"""
        data = {
            "parent_id": parent_id,
            "share_id": share_id,
            "pass_code_token": share_params.get('pass_code_token'),
            "ancestor_ids": [],
            "file_ids": file_ids,
            "specify_parent_id": True
        }
        response = await self.fetch_login_after(url="https://api-pan.xunlei.com/drive/v1/share/restore", data=data,
                                                return_response=True)

        if response.status_code == 200:
            self.log.info(f'成功转存 {len(file_ids)} 个文件到云盘目录ID：{parent_id}')
            return True
        else:
            self.log.error(f'转存失败：{response.json().get("error_description")}')
            return False
