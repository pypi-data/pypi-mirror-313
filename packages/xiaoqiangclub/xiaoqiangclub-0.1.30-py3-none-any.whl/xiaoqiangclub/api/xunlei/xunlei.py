# _*_ coding : UTF-8 _*_
# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/13 8:50
# 文件名称： api.py
# 项目描述： 迅雷API
# 开发工具： PyCharm
from xiaoqiangclub.api.xunlei.xunlei_cloud_disk import XunleiCloudDisk
from xiaoqiangclub.api.xunlei.xunlei_remote_downloader import XunleiRemoteDownloader


class Xunlei:
    def __init__(self, username: str, password: str):
        """
        Xunlei远程设备 API（微信公众号：XiaoqiangClub）

        :param username: 用户名
        :param password: 密码
        """

        # 远程下载
        self.remote_downloader = XunleiRemoteDownloader(username, password)

        self.log = self.remote_downloader.log  # 远程下载日志
        self.user_info = self.remote_downloader.get_user_info  # 获取用户信息

        self.downloader = self.remote_downloader.create_remote_download_task  # 创建远程下载任务
        self.download_from_yunpan = self.remote_downloader.create_remote_download_task_from_yunpan  # 将云盘中的文件使用远程设备下载

        self.get_device_tasks = self.remote_downloader.get_remote_device_tasks  # 获取指定远程设备的下载任务
        self.get_all_tasks = self.remote_downloader.get_all_remote_tasks  # 获取所有远程设备的下载任务
        self.get_devices = self.remote_downloader.get_all_remote_devices  # 获取所有远程设备
        self.device_is_online = self.remote_downloader.check_remote_device_is_online  # 检查远程设备是否在线
        self.pause_task = self.remote_downloader.pause_task
        self.start_task = self.remote_downloader.start_task
        self.delete_task = self.remote_downloader.delete_task
        self.set_download_num = self.remote_downloader.set_remote_download_num  # 设置远程设备同时下载任务的数量
        self.set_download_speed = self.remote_downloader.set_remote_download_speed  # 设置远程设备下载速度

        # 云盘
        self.cloud_disk = XunleiCloudDisk(username, password)

        self.yp_log = self.cloud_disk.log  # 云盘日志
        self.yp_downloader = self.cloud_disk.yunpan_create_download_task  # 云添加，将资源下载到云盘
        self.yp_space_info = self.cloud_disk.yunpan_get_space_info  # 获取云盘容量信息
        self.yp_offline_info = self.cloud_disk.yunpan_get_create_offline_task_limit  # 获取云盘创建离线任务次数上限

        self.yp_upload = self.cloud_disk.yunpan_upload_task  # 云盘上传文件
        self.yp_upload_file = self.cloud_disk.yunpan_upload_file  # 云盘上传文件
        self.yp_upload_dir = self.cloud_disk.yunpan_upload_folder  # 云盘上传文件夹

        self.yp_transfer = self.cloud_disk.yunpan_share_link_transfer  # 云盘分享资源转存
        self.yp_create_link_file = self.cloud_disk.yunpan_create_link_file_api  # 云盘新建链接文件
        self.yp_get_all_share_link = self.cloud_disk.yunpan_get_all_share_link  # 获取云盘所有的分享链接
        self.yp_create_share_link = self.cloud_disk.yunpan_create_share_link  # 获取云盘分享链接
        self.yp_search = self.cloud_disk.yunpan_search_resources  # 搜索云盘文件

        self.yp_folder_map = self.cloud_disk.yunpan_get_folder_map  # 导出指定云盘目录的结构信息到文件
        self.yp_clear_ads = self.cloud_disk.yunpan_clear_ads  # 遍历指定目录执行回调函数，可实现删除广告等功能
        self.yp_rename = self.cloud_disk.yunpan_rename  # 云盘文件/文件夹重命名
        self.yp_task_history = self.cloud_disk.yunpan_get_tasks_history  # 获取云盘的云添加任务历史信息
        self.yp_move = self.cloud_disk.yunpan_file_move  # 云盘文件/文件夹移动
        self.yp_copy = self.cloud_disk.yunpan_file_copy  # 云盘文件/文件夹复制
        self.yp_delete = self.cloud_disk.yunpan_file_delete  # 云盘文件/文件夹删除
        self.yp_create_folder = self.cloud_disk.yunpan_create_folders  # 云盘创建文件夹
        self.yp_exists = self.cloud_disk.yunpan_file_or_folder_exists  # 云盘文件/文件夹是否存在
        self.yp_recycle_bin_clear = self.cloud_disk.yunpan_recycle_bin_clear  # 清空云盘回收站
        self.yp_recycle_bin_restore = self.cloud_disk.yunpan_recycle_bin_restore  # 还原回收站文件
