from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.executors.pool import ProcessPoolExecutor

from .log_tools import logger

# REDIS_DB = {"db": 1, "host": "127.0.0.1"}


def func(name):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(now + f" Hello Openfund, {name}")


class OpenfundScheduler:
    scheduler_config = {
        # 配置存储器
        "apscheduler.jobstores.default": {
            "type": "sqlalchemy",
            "url": "sqlite:///jobs.sqlite",
        },
        # 配置执行器
        "executors": {
            # 使用进程池进行调度，最大进程数是10个
            "default": ProcessPoolExecutor(10)
        },
        # 创建job时的默认参数
        "job_defaults": {
            "coalesce": False,  # 是否合并执行
            "max_instances": 3,  # 最大实例数
        },
        "apscheduler.timezone": "Asia/Shanghai",
    }

    def __init__(self) -> None:

        self._scheduler = AsyncIOScheduler(**self.scheduler_config)

        # 添加一个定时任务
        self._scheduler.add_job(
            func,
            "interval",
            seconds=10,
            args=["Openfund-Keepalive"],
            id="Openfund_Keepalive_job",
            replace_existing=True,
        )

    @property
    def scheduler(self) -> BaseScheduler:
        return self._scheduler

    def start(self):
        self._scheduler.start()

    def stop(self):
        self._scheduler.shutdown()


scheduler = OpenfundScheduler().scheduler
