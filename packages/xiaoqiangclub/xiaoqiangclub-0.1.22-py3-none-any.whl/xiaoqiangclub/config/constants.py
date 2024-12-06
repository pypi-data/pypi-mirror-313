# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/26 18:01
# 文件名称： constants.py
# 项目描述： 常量
# 开发工具： PyCharm
import os
import platform
import tempfile

VERSION = '0.1.22'  # xiaoqiangclub模块版本号

# 项目根目录
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 模版存放目录
TEMPLATE_PATH = os.path.join(ROOT_PATH, 'templates')

# 当前运行的系统
CURRENT_SYSTEM = platform.system()

# pip镜像： 阿里云
PIP_MIRROR = 'https://mirrors.aliyun.com/pypi/simple/'

# 当前系统的临时文件目录路径
SYSTEM_TEMP_DIR = tempfile.gettempdir()
