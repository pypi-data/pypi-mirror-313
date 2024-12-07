from __future__ import annotations

import csv

from abc import abstractmethod
from pathlib import Path
from datetime import datetime

from .openfund import Openfund, openfund as op
from .scheduler import scheduler

# from .scheduler import scheduler
from .log_tools import logger
from .enums import KlineInterval


class Collector:
    def __init__(self, openfund: Openfund = None, jobId: str = None) -> None:

        self._jobId = jobId
        if self._jobId is None:
            self._jobId = f"{self.__class__.__name__}_{id(self)}"

        self._openfund = openfund
        if self._openfund is None:
            self._openfund = op

    @abstractmethod
    def collect(self) -> None:
        raise NotImplementedError()

    def job_function(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now + f"------ Hello world, {self._jobId}")
        logger.debug(now + f"------ Hello world, {self._jobId}-- debug")

    def start(
        self,
        interval: KlineInterval,
        jobId: str = "",
        func=None,
    ) -> int:
        job_kwargs = {}

        if jobId == "":
            job_kwargs["id"] = self._jobId
        else:
            job_kwargs["id"] = jobId

        job_kwargs["replace_existing"] = True
        job_kwargs["trigger"] = "interval"
        match interval.unitType:
            case "s":
                job_kwargs["seconds"] = interval.unit
            case "m":
                job_kwargs["minutes"] = interval.unit
            case "h":
                job_kwargs["hours"] = interval.unit
            case "d":
                job_kwargs["days"] = interval.unit
            case "w":
                job_kwargs["weeks"] = interval.unit
            case _:
                job_kwargs["seconds"] = 3

        job_kwargs["args"] = []

        if func is None:
            func = self.collect

        _job = scheduler.add_job(func=func, **job_kwargs)
        # Scheduler().scheduler.add_job(
        #     func=self.collect, trigger="interval", id=self._jobId, job_kwargs=job_kwargs
        # )
        logger.debug(f"---- Collector.start job is {_job.id}")
        if _job is not None:
            return 0
        else:
            return 1

    # 这个问题发生的原因可能是由于在使用poetry.utils.authenticator.Authenticator
    # 类时，尝试获取与给定URL相关的存储库配置，但由于某种原因，返回的对象与预期的对象不匹配。这可能是由于配置文件中的错误、网络问题或版本不兼容导致的。建议检查相关的配置文件和网络连接，确保使用的库版本是兼容的。

    def stop(self) -> int:
        scheduler.remove_job(self.jobName)
        logger.debug(f"{self._job.name} is stop .")
        return 0

    def pause(self) -> int:
        scheduler.pause()
        logger.debug(f"{self._job.name} is pause .")
        return 0

    def resume(self) -> int:
        scheduler.resume()
        logger.debug(f"{self._job.name} is resume .")
        return 0

    def _write_to_csv(self, file: Path, listData: list) -> None:

        # 如果路径不存在，创建路径
        file.parent.mkdir(parents=True, exist_ok=True)

        with open(file, "a", newline="") as file:
            writer = csv.writer(file)
            # 时间戳倒序，插入文件尾部
            writer.writerows(sorted(listData, key=lambda x: x[0], reverse=True))

        logger.debug("2、{}条写入{}文件...".format(len(listData), file))
