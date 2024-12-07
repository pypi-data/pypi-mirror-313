# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024-11-17
# 文件名称： crontab.py
# 项目描述： 封装apscheduler，实现常用后台执行定时任务，注释掉的是一些不常用的存储器，如果需要，可执行下载安装对应库，然后取消注释
# 开发工具： PyCharm
import inspect
from xiaoqiangclub.config.log_config import log
from typing import (Callable, Optional, Any, Dict)
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.events import (EVENT_JOB_EXECUTED, EVENT_JOB_ERROR)


def log_job_status(event) -> None:
    """
    记录任务执行状态的日志
    :param event: 事件对象
    """
    if event.exception:
        log.error(f"任务 {event.job_id} 执行失败：{event.traceback}")
    else:
        log.info(f"任务 {event.job_id} 执行成功！")


class MyCrontab:
    def __init__(self,
                 listener_handle: Optional[Callable] = log_job_status,
                 job_store_type: str = 'memory',
                 job_store_options: Optional[Dict[str, Any]] = None,
                 use_async_scheduler: bool = False) -> None:
        """
        初始化调度器

        :param listener_handle: 事件监听处理函数，默认为log_job_status
        :param job_store_type: 任务存储类型，默认为 'memory'。可选值包括 'memory', 'sqlalchemy', 'mongodb', 'redis', 'rethinkdb', 'zookeeper'
        :param job_store_options: 任务存储配置，例如数据库URL等。对于 'memory' 类型无需配置
        :param use_async_scheduler: 是否使用异步调度器，默认为False
        """
        log.debug(f"初始化 {'AsyncIOScheduler' if use_async_scheduler else 'BackgroundScheduler'} 调度器...")
        job_store_mapping = {
            'redis': RedisJobStore,
            # 'sqlalchemy': SQLAlchemyJobStore,
            # 'mongodb': MongoDBJobStore,
            # 'rethinkdb': RethinkDBJobStore,
            # 'zookeeper': ZooKeeperJobStore
        }

        if job_store_type in job_store_mapping:
            if not job_store_options:
                raise ValueError(f"缺少必要的 {job_store_type} 存储配置选项。请提供相关配置。")
            job_stores = {'default': job_store_mapping[job_store_type](**job_store_options)}
        elif job_store_type == 'memory':
            job_stores = None
        else:
            raise ValueError(f"不支持的任务存储类型: {job_store_type}")

        # 根据use_async_scheduler参数选择调度器
        if job_stores:
            self.scheduler = AsyncIOScheduler(jobstores=job_stores) if use_async_scheduler else BackgroundScheduler(
                jobstores=job_stores)
            log.debug(f"使用 {job_store_type} 存储，配置：{job_store_options}")
        else:
            self.scheduler = AsyncIOScheduler() if use_async_scheduler else BackgroundScheduler()
            log.debug("使用内存存储...")

        self.scheduler.add_listener(listener_handle, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    def start(self) -> None:
        """
        启动调度器
        """
        self.scheduler.start()
        log.debug("定时任务的调度器已启动，任务开始调度...")

    def stop(self) -> None:
        """
        停止调度器
        """
        self.scheduler.shutdown()
        log.debug("定时任务的调度器已停止，所有任务已暂停...")

    def add_job(self, func: Callable[..., Any], trigger: str, job_id: Optional[str] = None, coalesce: bool = True,
                **kwargs) -> None:
        """
        添加定时任务

        :param func: 任务函数，可以是同步或异步函数。
        :param trigger: 触发方式，支持以下类型：
            - 'interval': 按固定间隔执行任务。支持参数：
                - seconds: 间隔秒数（例如每 5 秒执行一次）。
                - minutes: 间隔分钟数（例如每 2 分钟执行一次）。
                - hours: 间隔小时数（例如每 1 小时执行一次）。
              示例：
                - 每 5 秒执行一次：'interval', seconds=5
                - 每 2 分钟执行一次：'interval', minutes=2
                - 每 1 小时执行一次：'interval', hours=1

            - 'cron': 按照 Cron 表达式的方式执行任务。支持参数：
                - minute: 分钟（0-59）
                - hour: 小时（0-23）
                - day: 日期（1-31）
                - month: 月份（1-12）
                - weekday: 星期几（0-6，其中 0=星期天）
              示例：
                - 每小时的第 15 分钟执行一次：'cron', minute=15
                - 每天的 8:00 执行一次：'cron', hour=8, minute=0
                - 每周一到周五的 9:00 执行一次：'cron', day_of_week='mon-fri', hour=9, minute=0
                - 每月的 1 号执行一次：'cron', day=1, hour=0, minute=0
                - 每年 12 月 25 日的 12:00 执行一次：'cron', month=12, day=25, hour=12, minute=0

            - 'date': 在指定的日期和时间执行一次任务。支持参数：
                - run_date: 任务执行的时间，必须是一个日期时间对象（如 datetime）。
              示例：
                - 在 2024 年 12 月 25 日的 12:00 执行一次：'date', run_date='2024-12-25 12:00:00'
                - 当前时间的 5 秒后执行一次：'date', run_date=datetime.now() + timedelta(seconds=5)

        :param job_id: 任务的唯一ID，默认为None，如果未指定，使用func的名称。
        :param coalesce: 是否合并错过的任务执行，默认为 True。如果为 True，将跳过的任务会被合并，执行一次。
        :param kwargs: 任务触发的具体配置，如 'interval' 触发器的 seconds 参数，'cron' 触发器的 hour, minute 参数等。
        """
        if trigger not in ['interval', 'cron', 'date']:
            raise ValueError(f"触发方式 {trigger} 不支持！请使用以下之一：'interval', 'cron', 'date'")

        # 如果未提供任务ID，使用func的名称作为默认ID
        if job_id is None:
            job_id = func.__name__

        kwargs['coalesce'] = coalesce  # 设置是否合并错过的任务

        # 如果是异步函数，使用asyncio调度
        if inspect.iscoroutinefunction(func):
            self.scheduler.add_job(func, trigger, id=job_id, **kwargs)
            log.info(
                f"已添加异步任务：{func.__name__}，任务ID：{job_id}，触发方式：{trigger}，触发参数：{kwargs}，合并错过任务：{coalesce}。")
        else:
            self.scheduler.add_job(func, trigger, id=job_id, **kwargs)
            log.info(
                f"已添加同步任务：{func.__name__}，任务ID：{job_id}，触发方式：{trigger}，触发参数：{kwargs}，合并错过任务：{coalesce}。")

    def remove_job(self, job_id: str) -> None:
        """
        移除任务
        :param job_id: 任务ID
        """
        try:
            self.scheduler.remove_job(job_id)
            log.info(f"已移除任务：{job_id}。")
        except JobLookupError:
            log.error(f"任务 {job_id} 不存在，无法移除。")

    def list_jobs(self) -> None:
        """
        列出所有定时任务
        """
        jobs = self.scheduler.get_jobs()
        if not jobs:
            log.info("当前没有任何定时任务。")
        for job in jobs:
            log.info(f"任务ID：{job.id}, 触发方式：{job.trigger}, 下一次执行时间：{job.next_run_time}, "
                     f"任务状态：{'激活' if job.next_run_time else '已停止'}")
