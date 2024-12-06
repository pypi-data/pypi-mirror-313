# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/26 18:10
# 文件名称： logger.py
# 项目描述： 使用 logging 模块写的日志模块
# 开发工具： PyCharm
import logging
from logging.handlers import TimedRotatingFileHandler
import os


class LoggerBase:
    LOG_LEVELS = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    def __init__(self, log_name: str = None, console_log_level: str = "DEBUG", file_log_level: str = "INFO",
                 log_file: str = None, log_when: str = 'midnight', log_interval: int = 1,
                 log_backup_count: int = 7,
                 log_format: str = '%(asctime)s - [%(name)s %(filename)s:%(lineno)d] - %(levelname)s： %(message)s'):
        """
        日志基类

        :param log_name: 日志记录器名称
        :param console_log_level: 控制台日志级别，默认为 DEBUG
        :param file_log_level: 文件日志级别，默认为 INFO
        :param log_file: 日志文件路径，自动保存 INFO 及以上级别的日志，默认为 None（即不保存到文件）
        :param log_when: 日志切割时间，默认为 'midnight'。支持的格式包括：
                         'S'：每隔几秒切割，例如，每 10 秒切割一次。
                         'M'：每隔几分钟切割，例如，每 5 分钟切割一次。
                         'H'：每隔几小时切割，例如，每 1 小时切割一次。
                         'D'：每天切割，例如，每 1 天切割一次。
                         'W0'-'W6'：每周几切割，例如，每周一（'W0'）切割一次。
                         'midnight'：每天午夜切割。
        :param log_interval: 日志切割间隔，默认为 1。例如，log_when='H' 且 log_interval=3，则表示每 3 小时切割一次日志。
        :param log_backup_count: 日志备份数量，默认为 7
        :param log_format: 日志显示格式，默认为：%(asctime)s - [%(name)s %(filename)s:%(lineno)d] - %(levelname)s: %(message)s
        """
        self.__validate_parameters(console_log_level, file_log_level, log_when)
        self.logger_name = log_name
        self.console_level = self.__get_log_level(console_log_level)
        self.file_level = self.__get_log_level(file_log_level)
        self.log_file = os.path.abspath(log_file) if log_file else None
        self.log_when = log_when
        self.log_interval = log_interval
        self.log_backup_count = log_backup_count
        self.log_format = log_format
        self.logger = self.__create_logger()

    @staticmethod
    def __get_log_level(level):
        """
        根据输入的日志级别返回对应的整型值。

        :param level: 输入的日志级别，可以是字符串或整型值
        :return: 对应的整型日志级别
        """
        if isinstance(level, int):
            return level
        level = level.upper()
        if level in LoggerBase.LOG_LEVELS:
            return LoggerBase.LOG_LEVELS[level]
        raise ValueError(f"日志级别无效，必须是以下之一：{list(LoggerBase.LOG_LEVELS.keys())} 或整型值。")

    @staticmethod
    def __validate_parameters(console_level: str, file_level: str, log_when: str):
        """
        验证输入参数的有效性。

        :param console_level: 控制台日志级别
        :param file_level:    文件日志级别
        :param log_when:      日志切割时间
        """
        valid_levels = LoggerBase.LOG_LEVELS.keys()

        # 处理控制台日志级别
        if isinstance(console_level, str) and console_level.upper() not in valid_levels and not isinstance(
                console_level, int):
            raise ValueError(f"控制台的日志级别无效。必须是以下之一：{valid_levels}.")

        # 处理文件日志级别
        if isinstance(file_level, str) and file_level.upper() not in valid_levels and not isinstance(file_level, int):
            raise ValueError(f"日志文件的日志级别无效。必须是以下之一：{valid_levels}.")

        supported_when = ['S', 'M', 'H', 'D', 'midnight'] + [f'W{i}' for i in range(7)]
        if log_when not in supported_when:
            raise ValueError(f"log_when 的值无效，必须是以下之一：{supported_when}.")

    def __create_logger(self) -> logging.Logger:
        """
        创建日志记录器并配置其处理器和格式。

        :return: 日志记录器对象
        """
        logger = logging.getLogger(self.logger_name)
        if not logger.hasHandlers():  # 防止重复添加处理器
            try:
                # 设置控制台日志处理器
                console_handler = logging.StreamHandler()
                console_formatter = logging.Formatter(self.log_format)
                console_handler.setFormatter(console_formatter)
                console_handler.setLevel(self.console_level)
                logger.addHandler(console_handler)

                # 设置文件日志处理器（如果有指定日志文件路径）
                if self.log_file:
                    # 创建日志文件目录
                    os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
                    file_handler = TimedRotatingFileHandler(
                        self.log_file, when=self.log_when, interval=self.log_interval,
                        backupCount=self.log_backup_count, encoding='utf-8')
                    file_formatter = logging.Formatter(self.log_format)
                    file_handler.setFormatter(file_formatter)
                    file_handler.setLevel(self.file_level)
                    logger.addHandler(file_handler)

                # 设置日志级别
                logger.setLevel(min(self.console_level, self.file_level))
            except Exception as e:
                logger.error(f"设置日志记录器时发生错误: {e}", exc_info=True)
        return logger

    def set_log_level(self, level: str):
        """
        动态设置日志级别。

        :param level: 日志级别，可以是字符串或整型值
        """
        new_level = self.__get_log_level(level)
        self.logger.setLevel(new_level)
        for handler in self.logger.handlers:
            handler.setLevel(new_level)
