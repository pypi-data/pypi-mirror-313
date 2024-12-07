# _*_ coding : UTF-8 _*_
# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/10 12:47
# 文件名称： xunlei_remote_downloader.py
# 项目描述： 迅雷远程（https://pan.xunlein.com/yc）的接口，可调用接口实现给远程设备添加下载任务等操作
# 开发工具： PyCharm
import asyncio
from typing import (Optional, Dict, List, Union)
from xiaoqiangclub.api.xunlei.xunlei_base import XunleiBase


class XunleiRemoteDownloader(XunleiBase):
    def __init__(self, username: str, password: str):
        """
        Xunlei远程设备 API（微信公众号：XiaoqiangClub）

        :param username: 用户名
        :param password: 密码
        """
        super().__init__(username=username, password=password)

    async def __get_remote_tasks(self, remote_device: str = None) -> Optional[dict]:
        """
        获取远程设备/远程设备的任务详情:
        当 remote_device 为空，则获取所有设备详情；
        当 remote_device 不为空，则获取单个设备的所有任务详情。

        :param remote_device: 远程设备的名称（例如：电脑-XiaoqiangClub）或远程设备的device_id（例如："device_id#57200b9b0a4495b38e759e282b4ac0e4"）
        :return:
        """
        if remote_device is None:
            params = {
                "type": "user#runner",
                "space": ""
            }
        else:
            # 判断用户输入的是设备名称还是设备ID
            if remote_device.startswith('device_id'):
                remote_device_id = remote_device
            else:
                remote_device_id = self.common.get(remote_device, {}).get('remote_device_id')
                if not remote_device_id:
                    # 从所有远程设备中查询
                    await self.get_all_remote_devices()
                    remote_device_id = self.common.get(remote_device, {}).get('remote_device_id')

                if not remote_device_id:
                    self.log.error(f'未找到远程设备 {remote_device} 的设备ID！')
                    return None

            params = {"space": remote_device_id}

        return await self.fetch_login_after(url="https://api-pan.xunlei.com/drive/v1/tasks", params=params)

    async def __get_remote_device_id(self, remote_name: str, return_id: bool = False) -> Optional[str]:
        """
        获取远程下载设备的 id   device_id

        :param remote_name: 远程下载设备的名称，例如：电脑-XiaoqiangClub
        :param return_id: 是否返回id（VO8Z54hRueox1x4K6lvhJMfeA1），默认返回device_id（device_id#57200b9b0a4495b38e759e282b4ac0e4）
        :return: 设备的 device_id，如果未找到则返回 None
        """
        if return_id:
            get_key = 'remote_id'
        else:
            get_key = 'remote_device_id'

        need_id = self.common.get(remote_name, {}).get(get_key)

        # 如果 device_id 为空，则获取所有设备信息
        if need_id is None:
            await self.get_all_remote_devices()
            need_id = self.common.get(remote_name, {}).get(get_key)

        # 检查是否找到了 device_id
        if need_id is None:
            self.log.error(f'未找到 {remote_name} 对应的 device_id，请检查是否正确填写了远程下载设备的名称')

        return need_id

    async def __get_remote_device_name(self, remote_device_id: str) -> Optional[str]:
        """
        使用远程设备ID获取设备名称

        :param remote_device_id: 远程设备的 device_id（例如："device_id#57200b9b0a4495b38e759e282b4ac0e4"）
        :return: 设备名称或 None
        """
        # 判断是否已经登录
        await self.login()

        # 尝试从缓存中获取设备名称
        device_name = self.common.get(remote_device_id)
        if device_name:
            self.log.debug(f'使用远程设备ID {remote_device_id} 查询到设备的名称为：{device_name}')
            return device_name

        # 从所有远程设备中查询
        all_devices = await self.get_all_remote_devices()

        # 使用字典推导快速查找设备名称
        device_map = {device['remote_client_id']: device['remote_name'] for device in all_devices}

        # 检查是否找到设备名称
        device_name = device_map.get(remote_device_id)
        if device_name:
            # 缓存设备信息
            self.common[remote_device_id] = device_name
            self.log.debug(f'使用远程设备ID {remote_device_id} 查询到设备的名称为：{device_name}')
            return device_name

        self.log.error(f'未找到远程设备 {remote_device_id} 的名称！')
        return None

    async def get_remote_device_tasks(self, remote_device: str, return_raw_data: bool = False) -> Optional[list]:
        """
        获取指定远程设备的任务列表

        :param remote_device: 远程设备的名称，区分大小写，（例如：电脑-XiaoqiangClub）或远程设备的device_id（例如："device_id#57200b9b0a4495b38e759e282b4ac0e4"）
        :param return_raw_data: 是否返回所有原始数据，默认为 False，返回主要信息
        :return:
        """
        # 判断是否已经登录
        await self.login()

        self.log.debug(f'获取远程设备 {remote_device} 的任务列表...')
        json_data = await self.__get_remote_tasks(remote_device)

        if not json_data:
            return None

        if return_raw_data:
            return json_data

        tasks = json_data.get('tasks', [])
        all_tasks = []
        for task in tasks:
            params = task.get('params', {})
            all_tasks.append({
                # 后续任务操作要用到：暂停、开始等需要用到的参数
                'task_processing_params': {
                    'id': task.get('id'),  # [后续任务操作要用到：暂停、开始等]任务id：VO8UA033QK6sT7_g6qmLTNHgA1
                    # [后续任务操作要用到：暂停、开始等]存储设备id：device_id#57200b9b0a4495b38e759e282b4ac0e4
                    'space': task.get('space'),
                    'type': task.get('type'),  # [后续任务操作要用到：暂停、开始等]任务类型："type": "user#download-url"
                },
                'download_url': params.get('url'),  # 下载链接
                'file_name': task.get('name'),  # 文件名：下载任务保存的文件名
                'save_path': params.get('real_path'),  # 保存路径
                'parent_folder_id': params.get('parent_folder_id'),  # 父文件夹id
                'total_file_count': params.get('total_file_count'),  # 文件数量
                'finish': task.get('message') == "完成",  # 状态: "完成","任务超时，请重试"
                'progress': task.get('progress'),  # 进度
                'message': task.get('message'),  # 状态信息："已添加","任务超时，请重试"
                'phase': task.get('phase'),  # 状态："PHASE_TYPE_RUNNING"
            })
        return all_tasks

    async def get_all_remote_tasks(self) -> Optional[Dict[str, list]]:
        """获取所有设备的任务数据"""
        await self.login()

        self.log.debug('获取所有设备的任务数据...')
        all_devices = await self.get_all_remote_devices()

        # 创建一个字典来存储结果
        tasks = {}

        async def get_and_store_tasks(device_id):
            remote_name = device_id.get('remote_name')  # 远程设备名称
            remote_client_id = device_id.get('remote_client_id')  # 获取设备ID
            tasks[remote_name] = await self.get_remote_device_tasks(remote_client_id)

        # 并发执行所有任务，并将结果存储在字典中
        await asyncio.gather(*[get_and_store_tasks(device_id) for device_id in all_devices])
        self.log.debug(f'获取所有设备的任务数据：{tasks}')
        return tasks

    async def get_all_remote_devices(self, return_raw_data=False) -> Optional[list]:
        """
        获取所有远程下载设备信息

        :return_raw_data: 是否返回原始数据，默认只返回设备名称和device_id等主要信息
        :return:
                [{'remote_client_id': 'device_id#57200b9b0a4495b38e759e282b4ac0e4',
                'remote_name': '电脑-XiaoqiangClub'},
                {'remote_client_id': 'device_id#bd4a89bb8ff9af7b443490884afd9381',
                'remote_name': '群晖-Xunlei'}]
        """
        # 判断是否已经登录
        await self.login()

        self.log.debug('获取所有远程下载设备信息...')
        device_info = await self.__get_remote_tasks()

        if device_info:
            info_list = device_info.get('tasks')
            all_remote_devices = []  # 所有远程下载设备信息

            for info in info_list:
                remote_name = info.get('name')  # 远程设备名称
                remote_id = info.get('id')  # 远程设备id
                remote_device_id = info.get('params').get('target')  # 远程设备的device_id
                remote_info = {
                    'remote_name': remote_name,
                    'remote_client_id': remote_device_id,  # device_id#57200b9b0a4495b38e759e282b4ac0e4
                    'id': remote_id,  # VO8U3vJSLFU_91eoZL9m56uAA1
                    'client_id': info.get('params').get('client_id'),  # XW-G4v1H72tgfJym
                    'product_name': info.get('params').get('product_name')
                }
                all_remote_devices.append(remote_info)
                # 保存到 self.common
                self.common.setdefault(remote_name, {})['remote_device_id'] = remote_device_id
                self.common.setdefault(remote_name, {})['remote_id'] = remote_id

                # 方便使用远程设备id查询设备名称
                self.common[remote_device_id] = remote_name

            if return_raw_data:
                self.log.debug(f'获取到所有远程下载设备信息：{device_info}')
                return device_info

            self.log.debug(f'获取到所有远程下载设备信息：{all_remote_devices}')
            return all_remote_devices

    async def check_remote_device_is_online(self, remote_name: str) -> bool:
        """
        检查远程下载设备是否在线

        :param remote_name: 远程下载设备的名称，区分大小写，例如：电脑-XiaoqiangClub
        :return:
        """
        await self.login()

        self.log.debug(f'检查远程设备 {remote_name} 是否在线...')
        if await self.__get_inner_api_url(remote_name):
            self.log.info(f'远程设备 {remote_name} 在线。')
            return True

        self.log.info(f'远程设备 {remote_name} 不在线。')
        return False

    async def __get_inner_api_url(self, remote_name: str) -> Optional[str]:
        """
        获取远程下载设备的API接口链接，同时也可以判断远程下载设备是否在线。

        :param remote_name: 远程下载设备的名称，例如：电脑-XiaoqiangClub  群晖-Xunlei
        :return:
        """
        await self.login()

        remote_device_id = await self.__get_remote_device_id(remote_name)
        url = "https://api-pan.xunlei.com/drive/v1/apps/INNER_API"
        params = {"space": remote_device_id}
        json_data = await self.fetch_login_after(url=url, params=params, max_retries=1)  # 最多重试一次，不需要重新登入
        if json_data:
            # 存储到 self.common
            inner_api = json_data.get('link')
            self.common.setdefault(remote_name, {})['inner_api'] = inner_api

            return inner_api
        else:
            self.log.error(f"获取 {remote_name} 的 inner_api 失败，请手动检查设备是否在线。")
            return None

    async def __get_remote_dir_info(self, remote_name: str, parent_folder_id: str = "") -> Optional[
        List[Dict[str, str]]]:
        """
        获取远程下载设备，指定目录下的文件夹信息（文件夹id等，无法获取文件信息）

        :param remote_name: 远程下载设备的名称，例如：电脑-XiaoqiangClub  群晖-Xunlei
        :param parent_folder_id: 父级目录的ID，默认为空字符串""：获取所有顶级根目录的 folder_id
        :return: 目录下所有文件夹的folder_id
        """
        self.log.debug(f'获取远程设备 {remote_name} 下 {parent_folder_id} 目录信息...')
        link = self.common.get(remote_name, {}).get('inner_api')
        if not link:
            link = await self.__get_inner_api_url(remote_name)

        if link:
            device_id = await self.__get_remote_device_id(remote_name)
            base_url = link.split('?')[0]
            url = base_url + "drive/v1/files"
            params = {
                "space": device_id,
                "parent_id": parent_folder_id,
                "plugin_app_token": link.split('plugin_app_token=')[-1],
                "device_space": "",
                # "limit": "20",  # 遍历目录的数量，系统默认是20，注释掉可以全部遍历
                "with_audit": "true",
                "filters": "{\"trashed\":{\"eq\":false},\"phase\":{\"eq\":\"PHASE_TYPE_COMPLETE\"},\"kind\":{\"eq\":\"drive#folder\"}}",
                "page_token": "",
                "with": "withCategoryDiskMountPath",  # 磁盘挂载路径
                # "with": "withCategoryDriveCachePath",# 缓存路径
                # "with": "withCategoryHistoryDownloadPath",# 历史下载路径
                # "with": "withReadOnlyFS",# 只读文件系统
                "order": "TYPE_DESC",
                "plugin_app_id": "INNER_API",
            }

            json_data = await self.get_response(url=url, params=params)
            # 整理数据
            dir_list = []
            for f in json_data.get('files'):
                params = f.get('params')
                # 剩余容量
                left_size = int(params.get('limit')) - int(params.get('usage'))

                dir_list.append({
                    'id': f.get('id'),  # 文件夹ID
                    'dir_path': params.get('RealPath'),  # 目录路径
                    'left_size': left_size,  # 剩余容量
                    'writable': params.get('is_write'),  # 是否可写
                })
            self.log.debug(f'获取远程下载设备 {remote_name} 下 {parent_folder_id} 的目录信息：{dir_list}')
            return dir_list
        else:
            self.log.error(f'错误！远程下载设备 {remote_name} 可能已经离线！')

    async def __get_remote_parent_folder_info(self, remote_name: str, target_folder: str) -> Optional[Dict[str, str]]:
        """
        获取远程下载设备指定文件夹的 id、left_size 等信息

        :param remote_name: 远程下载设备的名称，例如：电脑-XiaoqiangClub  群晖-Xunlei
        :param target_folder: 目标文件夹名称（下载的文件需要存放的文件夹路径）
        :return: 目标文件夹的 id，如果未找到则返回 None
        """
        # 获取顶级目录的 folder_id
        root_dirs = await self.__get_remote_dir_info(remote_name)
        if not root_dirs:
            return None

        # 将目标文件夹路径转换为列表
        target_parts = await self.split_path(target_folder, change_to_lower=True)

        # 检查顶级目录是否与目标文件夹相同
        for dir in root_dirs:
            if await self.split_path(dir.get('dir_path'), change_to_lower=True) == target_parts:
                self.log.debug(f'获取远程下载设备 {remote_name} 下 {target_folder} 的目录信息：{dir}')
                return dir

        parent_folder_id = ""  # 用于保存当前目录的ID和剩余容量
        flag_dir = []  # 当前判断路径的部分
        match_dir_info = None  # 匹配到的路径信息

        for index, part in enumerate(target_parts):
            flag_dir.append(part)

            # 获取当前父目录的子目录
            if index > 0:
                root_dirs = await self.__get_remote_dir_info(remote_name, parent_folder_id)

            # 在当前层级查找匹配的目录
            matched = False  # 标记当前层级是否找到匹配
            for dir in root_dirs:
                current_dir_parts = await self.split_path(dir.get('dir_path'), change_to_lower=True)
                if flag_dir == current_dir_parts:
                    parent_folder_id = dir.get('id')
                    matched = True
                    match_dir_info = dir  # 保存匹配到的路径信息
                    break  # 找到后跳出当前层级的循环

            # 如果当前层级没有找到匹配，返回 None
            if not matched:
                self.log.error(f'未找到远程下载设备 {remote_name} 下的 {target_folder}，请检查路径是否正确！')
                return None

        self.log.debug(f'获取远程下载设备 {remote_name} 下 {target_folder} 的目录信息：{match_dir_info}')
        return match_dir_info

    async def __manage_task(self, remote_device: str, spec: str, download_url: str = None) -> None:
        """
        下载任务操作：管理已添加的任务，任务类型: pause（暂停）、running（开始）、delete（删除）

        :param remote_device: 远程设备的名称（例如：电脑-XiaoqiangClub）或远程设备的 device_id（例如："device_id#57200b9b0a4495b38e759e282b4ac0e4"）
        :param spec: 任务类型: pause（暂停）、running（开始）、delete（删除）
        :param download_url: 任务链接（可选），如果为 None，将对所有任务执行操作
        :return:
        """
        await self.login()

        tasks = await self.get_remote_device_tasks(remote_device)

        async def process_task(t):
            data = t.get('task_processing_params')
            data.update({"set_params": {
                "spec": f'{{"phase":"{spec}"}}'  # 使用格式化字符串
            }})
            if spec == 'pause':
                self.log.info(f'暂停下载任务：{t.get("download_url")}')
            elif spec == 'running':
                self.log.info(f'开始下载任务：{t.get("download_url")}')
            elif spec == 'delete':
                self.log.info(f'删除下载任务：{t.get("download_url")}')
            await self.fetch_login_after(url="https://api-pan.xunlei.com/drive/v1/task", data=data, patch=True)

        if tasks:
            if download_url:  # 如果指定了下载链接，处理单个任务
                for t in tasks:
                    if t.get('download_url') == download_url:
                        await process_task(t)
                        return
                self.log.error(f'在 {remote_device} 未找到任务链接为 {download_url} 的任务！')
            else:  # 如果没有指定链接，处理所有任务
                # 只处理具有有效 download_url 的任务
                valid_tasks = [t for t in tasks if t.get('download_url') is not None]
                if valid_tasks:
                    await asyncio.gather(*(process_task(t) for t in valid_tasks))
                else:
                    self.log.warning(f'在 {remote_device} 没有可处理的任务！')

    async def pause_task(self, remote_device: str, download_url: str = None) -> None:
        """
        下载任务操作：暂停指定的下载任务或所有任务

        :param remote_device: 远程设备的名称（区分大小写）或远程设备的 device_id
        :param download_url: 任务链接（可选），如果为 None，将暂停所有任务
        :return:
        """
        return await self.__manage_task(remote_device, 'pause', download_url)

    async def start_task(self, remote_device: str, download_url: str = None) -> None:
        """
        下载任务操作：开始指定的下载任务或所有任务

        :param remote_device: 远程设备的名称（区分大小写）或远程设备的 device_id
        :param download_url: 任务链接（可选），如果为 None，将开始所有任务
        :return:
        """
        return await self.__manage_task(remote_device, 'running', download_url)

    async def delete_task(self, remote_device: str, download_url: str = None) -> None:
        """
        下载任务操作：删除指定的下载任务或所有任务

        :param remote_device: 远程设备的名称（区分大小写）或远程设备的 device_id
        :param download_url: 任务链接（可选），如果为 None，将删除所有任务
        :return:
        """
        return await self.__manage_task(remote_device, 'delete', download_url)

    async def __get_yunpan_dir_info(self, parent_folder_id: str = "", return_raw_data: bool = False) -> Optional[
        List[Dict]]:
        """
        获取云盘文件夹信息：文件/目录id等

        :param return_raw_data: 是否返回原始数据，默认为False，只返回主要信息
        :param parent_folder_id: 父级目录的ID，默认为空字符串""：获取云盘顶级根目录的 folder_id
        :return:
        """
        self.log.debug(f'正在获取云盘父级目录ID：{parent_folder_id} 的文件夹信息...')

        url = "https://api-pan.xunlei.com/drive/v1/files"
        params = {"parent_id": parent_folder_id}
        json_data = await self.fetch_login_after(url=url, params=params)

        if json_data:
            if return_raw_data:
                return json_data

            yunpan_dirs = []
            for file in json_data.get('files', []):
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
            return yunpan_dirs

    async def __get_yunpan_resource_info(self, target_folder: str) -> Optional[Dict]:
        """
        获取云盘指定文件/目录信息id 等

        :param target_folder: 目标文件/文件夹夹名（例如：我的转存）
        :return:
        """
        # 将目标文件夹路径转换为列表
        target_parts = await self.split_path(target_folder, change_to_lower=True)

        parent_folder_id = ""  # 用于保存当前目录的ID
        match_dir_info: Optional[Dict] = None  # 匹配到的路径信息
        for part in target_parts:
            # 获取顶级目录的 folder_id
            root_dirs = await self.__get_yunpan_dir_info(parent_folder_id)
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

        self.log.debug(f"匹配到 {target_folder} 的信息：{match_dir_info}")
        return match_dir_info

    async def set_remote_download_num(self, num: int, device_name: str) -> Optional[bool]:
        """
        设置远程设备同时下载任务的数量，只支持Nas等设备，不支持电脑

        :param num: 要设置的远程下载任务数量: 1-5
        :param device_name: 设备名称，区分大小写，例如："群晖-Xunlei"
        :return:
        """
        # 判断是否已经登录
        await self.login()

        self.log.debug(f'正在设置远程设备 {device_name} 的远程下载任务数量为：{num} ...')

        # 获取设备id
        device_id = await self.__get_remote_device_id(device_name)
        # 获取inner_api 接口。
        inner_api_url = await self.__get_inner_api_url(device_name)

        if device_id and inner_api_url:

            params = {
                "device_space": "",
                "space": device_id,  # 设备id
                "plugin_app_id": "INNER_API",
                "plugin_app_token": inner_api_url.split('plugin_app_token=')[-1]
            }

            # 限制数字在1-5
            num = min(max(num, 1), 5)

            data = {
                "runner_count": num
            }

            base_url = inner_api_url.split('?')[0]
            url = base_url + "device/config"

            json_data = await self.get_response(url=url, params=params, data=data)
            self.log.debug(f'设置远程设备 {device_name} 的远程下载任务数量为 {num} 的返回数据: {json_data}')

            if json_data:
                if json_data.get('runner_count') == num:
                    self.log.info(f'设置远程设备 {device_name} 的远程下载任务数量为：{num} 成功！')
                    return True
                else:
                    self.log.error(f'设置远程设备 {device_name} 的远程下载任务数量为：{num} 失败！')
                    return False

            return False

        else:
            self.log.error(f'设置下载任务数量失败，无法获取设备{device_name}的id')
            return False

    async def set_remote_download_speed(self, speed: float, device_name: str) -> Optional[bool]:
        """
        设置远程设备的下载限速（实际数值会有一定的偏差），只支持Nas等设备，不支持电脑

        :param speed: 单位：兆每秒（Mbps)，1Mbps = 1024KB/s。范围：0.06M/s（60kb/s） — 131.3M/s，-1 表示不限速
        :param device_name: 设备名称，区分大小写，例如："群晖-Xunlei"
        :return:
        """
        # 判断是否已经登录
        await self.login()

        # 限制数值在0.06M/s（60kb/s） — 131.3M/s
        speed = min(max(speed, 0.06), 131.3)

        # 转换为字节
        speed = int(speed * 1024 * 1024)

        self.log.debug(f'正在设置远程设备 {device_name} 的下载限速为：{speed} 字节/秒 ...')
        need_id = await self.__get_remote_device_id(device_name, return_id=True)

        if need_id:
            data = {
                "type": "user#runner",
                "id": need_id,
                "set_params": {
                    "set_device_config": f'{{"speed_limit":{speed}}}'  # 使用变量
                }
            }
            json_data = await self.fetch_login_after(url="https://api-pan.xunlei.com/drive/v1/task",
                                                     data=data, patch=True)

            if json_data == {}:
                self.log.info(f'设置远程设备 {device_name} 的下载限速为：{speed} 字节/秒 成功！')
                return True

        self.log.error(f'设置远程设备 {device_name} 的下载限速为：{speed} 字节/秒 失败！')
        return False

    async def create_remote_download_task_from_yunpan(self, remote_name: str, target_folder: str,
                                                      download_yunpan_resource: str,
                                                      rename: str = None) -> Optional[Dict]:
        """
        下载迅雷云盘中的资源，例如：将保存在云盘中的电影通过远程设备进行下载。

        :param remote_name: 远程下载设备名称，例如："群晖-Xunlei"， 需保证该设备已经登录。
        :param target_folder: 下载的资源保存到远程下载设备的目标文件夹路径
        :param download_yunpan_resource: 需要下载的云盘文件/目录路径："我的转存/电影/xxx.mp4"，"我的转存/电影"（目录）
        :param rename: 文件/目录重命名，默认为云盘中原来的名称
        :return:
        """
        # 判断是否已经登录
        await self.login()

        self.log.debug(f'创建任务：下载云盘资源 {download_yunpan_resource} 到 {remote_name} 的 {target_folder} ...')
        device_id = await self.__get_remote_device_id(remote_name)
        target_folder = await self.__get_remote_parent_folder_info(remote_name, target_folder)
        yunpan_resource = await self.__get_yunpan_resource_info(download_yunpan_resource)

        if device_id and yunpan_resource and target_folder:

            rename = rename or yunpan_resource.get('name')

            data = {
                "space": device_id,  # 设备id
                "type": "user#download",
                "file_name": rename,
                "file_size": yunpan_resource.get('size', ""),
                "params": {
                    "target": device_id,
                    "file_id": yunpan_resource.get('id'),
                    "parent_folder_id": target_folder.get('id')  # 资源下载到目标文件夹的id
                }
            }
            json_data = await self.fetch_login_after(url="https://api-pan.xunlei.com/drive/v1/task", data=data)
            if json_data:
                self.log.info(
                    f'创建远程设备 {remote_name} 下载云盘资源 {download_yunpan_resource} 到 {target_folder} 的任务添加成功！')
                return json_data
            else:
                self.log.error(
                    f'创建远程设备 {remote_name} 下载云盘资源 {download_yunpan_resource} 到 {target_folder} 的任务添加失败！')
                return None
        else:
            self.log.error(f'创建下载云盘资源任务 {download_yunpan_resource} 失败！')

    async def create_remote_download_task(self, download_url: Union[str, List[str]], remote_name: str,
                                          target_folder: str, rename: Union[str, List[str]] = None,
                                          download_same_url: bool = False,
                                          sub_file_index: Union[List[str], List[List[str]]] = None) -> List[str]:
        """
        创建远程设备下载任务，如电影磁力链接下载等（https://pan.xunlei.com/yc），支持批量创建

        :param download_url: 下载链接，支持单个或批量：['magnet:?xt=urn:btih:41...',...]，资源类型：磁力链接/http链接/ed2k链接等，也可以传入BT文件的绝对路径，例如：/Users/xxx/Downloads/xxx.torrent
        :param remote_name: 远程下载设备的名称，区分大小写，例如：电脑-XiaoqiangClub, 群晖-Xunlei，需保证该设备已经登录。
        :param target_folder: 下载的文件要保存到的文件夹路径
        :param rename: 自定义保存的文件名，默认为None，表示使用下载链接中的文件名，支持单个或批量：['文件名1', '文件名2']
        :param download_same_url: 已经下载过的链接是否重新下载，默认为False，表示跳过以前下过的链接任务
        :param sub_file_index: 当链接包含多个文件的时候，可以设置需要下载的文件序号（从1开始），例如：[['1', '2'], ['3']], None表示全部
        :return: 创建失败的 download_url 列表
        """
        # 判断是否已经登录
        await self.login()

        # 如果 download_url 是字符串，转换为列表
        if isinstance(download_url, str):
            download_url = [download_url]

        # 将.torrent文件转换为 magnet链接
        for i, url in enumerate(download_url):
            if url.endswith('.torrent'):
                magnet, _ = await self.parse_torrent(url)
                download_url[i] = magnet

        # 如果 rename 是字符串，转换为列表
        if isinstance(rename, str):
            rename = [rename]

        # 检查远程设备是否在线
        if not await self.check_remote_device_is_online(remote_name):
            self.log.error(f'远程设备 {remote_name} 不在线，无法创建下载任务！')
            return download_url

        # 获取远程下载设备的 device_id
        device_id = await self.__get_remote_device_id(remote_name)

        # 判断哪些任务已经存在
        existing_tasks = await self.get_remote_device_tasks(device_id)
        existing_urls = {task.get('download_url') for task in existing_tasks}

        # 提前判断是否所有URL已存在/下载过
        if all(url in existing_urls for url in download_url) and not download_same_url:
            self.log.info('您所添加的任务都已存在/已下载，无需重新添加')
            return []

        # 获取目标文件夹的 folder_id 等信息
        target_folder_info = await self.__get_remote_parent_folder_info(remote_name, target_folder)
        if not target_folder_info:
            return download_url if isinstance(download_url, list) else [download_url]

        device_left_size = int(target_folder_info.get('left_size'))  # 目标文件夹剩余空间

        tasks = []  # 创建下载任务的异步任务列表
        failed_urls = []  # 创建失败的 download_url 列表
        existing_urls_count = 0  # 已存在的任务数量

        for index, url in enumerate(download_url):
            if url in existing_urls and not download_same_url:
                self.log.info(f'任务已存在，跳过创建：{url}')
                existing_urls_count += 1
                continue

            self.log.debug(f'创建下载任务：{url}，保存路径：{target_folder}...')

            download_url_info = await self.get_download_url_info(url)  # 获取下载url的参数
            if not download_url_info:
                self.log.error('未能获取下载链接信息，无法创建任务！')
                failed_urls.append(url)
                continue
            task_size = int(download_url_info.get('task_size', '1073741824'))  # 任务大小:有一些任务无法获取任务大小就默认为1G
            if task_size > device_left_size:
                self.log.error('目标文件夹剩余空间不足，无法创建任务！')
                failed_urls.extend(download_url[index:])  # 后续的任务都无法创建
                break

            # 预留任务空间
            device_left_size -= task_size

            current_save_title = rename[index].strip() if rename else None
            if current_save_title is None:  # 如果没有自定义保存文件名，则使用下载链接中的文件名
                current_save_title = download_url_info.get('task_name')

            # 整理需要下载的子集索引
            file_count = download_url_info.get('file_count')
            if file_count > 1:
                if sub_file_index is None:  # 未设置子集，则下载全部
                    sub_file_index_str = f'{0},{int(file_count) - 1}'
                else:
                    sub_file_index_str = await self.format_sub_file_index(sub_file_index[index])
            else:
                sub_file_index_str = "0"

            data = {
                "file_name": current_save_title,  # 文件名
                "file_size": task_size,  # 文件大小，字节B
                "space": device_id,  # 空间
                "type": "user#download-url",  # 类型
                "params": {
                    "parent_folder_id": target_folder_info.get('id'),  # 父文件夹id
                    "target": device_id,  # 目标设备
                    "platform": "web",
                    "total_file_count": str(file_count),  # 文件总数，需要是字符串
                    "url": url,  # 需要下载的任务链接
                    "sub_file_index": sub_file_index_str  # 多集的资源需要下载的索引
                }
            }

            tasks.append((url, self.fetch_login_after(url="https://api-pan.xunlei.com/drive/v1/task", data=data)))

        # 等待所有任务完成并获取结果
        results = await asyncio.gather(*[task[1] for task in tasks], return_exceptions=True)

        # 统计结果
        success_count = 0
        failure_count = 0

        for index, result in enumerate(results):
            url, _ = tasks[index]
            if isinstance(result, dict):
                task_message = result.get('task', {}).get('message')
                if task_message == '等待中':
                    self.log.info(f"远程设备下载任务：{url} 下载到远程设备 {remote_name} 的 {target_folder} 创建成功！")
                    success_count += 1
                else:
                    self.log.error(
                        f"远程设备下载任务：{url} 下载到远程设备 {remote_name} 的 {target_folder} 创建失败！{result}")
                    failure_count += 1
                    failed_urls.append(url)
            else:
                failure_count += 1
                failed_urls.append(url)

        self.log.info(
            f"任务清单：总任务：{len(download_url)} 个，成功 {success_count} 个，失败 {failure_count} 个，已存在 {existing_urls_count} 个。")

        if failure_count > 0:
            self.log.error(f"任务创建失败的 URL: {failed_urls}")
        return failed_urls
