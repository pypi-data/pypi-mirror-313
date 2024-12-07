# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/27 6:44
# 文件名称： log_config.py
# 项目描述： 工具箱日志配置
# 开发工具： PyCharm
from xiaoqiangclub.utils.logger import LoggerBase

logger_xiaoqiangclub = LoggerBase(log_name="XiaoqiangClub", console_log_level='INFO')
log = logger_xiaoqiangclub.logger
