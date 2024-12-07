from __future__ import annotations

import time
from pathlib import Path
from datetime import datetime


from core.openfund.log_tools import logger
from core.openfund.enums import KlineInterval
from core.openfund.base_tool import Tool as BaseTool
from core.openfund.base_collector import Collector as BaseCollector
from core.openfund.time_tools import TimeTools


class KLinesCollectorEntity(BaseCollector):
    def __init__(
        self,
        hisSwitch: int = 0,
        hisDateTime: int = 0,
        pool: list = None,
        interval: int = 5,
        *,
        client: BaseTool,
    ) -> None:
        logger.debug("+++++++++++++++ KLinesCollector init +++++++++++++ ")
        super().__init__()
        self._pool = pool
        if self._pool is None:
            self._pool = ["BTCUSDT", "ETHUSDT"]

        self._interval = interval
        self._hisSwitch = hisSwitch
        self._hisDateTime = hisDateTime
        self._dataDir = self._openfund.dataDir
        self._client = client

    def job_function(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now + f"------ Hello world, {self._jobId}")
        logger.debug(now + f"------ Hello world, {self._jobId}-- debug")

    def collect(self) -> None:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now + f"------ collect, {self._jobId}")
        for symbol in self._pool:
            logger.debug("{} symbol 开始 ++++++++++++++++++++++++++++ ".format(symbol))
            latestRecords = 1  # 采集最近一次的记录数量
            records = 0  # 累计记录数
            queryCount = 0  # 执行次数
            nextEndTime = 0
            params = {"limit": 1000}
            while latestRecords != 0:  # 循环读取，直到记录为空
                queryCount += 1
                if nextEndTime != 0:
                    params = {"limit": 1000, "endTime": nextEndTime}

                logger.debug("1、{}第{}次开始执行...".format(symbol, queryCount))
                listData = []
                try:
                    listData = self._client.klines(
                        symbol,
                        KlineInterval.getByUnit(self._interval, "m"),
                        **params,
                    )
                except Exception as e:
                    # print("Error:", e)
                    logger.error(e)
                    time.sleep(10)
                    continue

                latestRecords = len(listData)
                data_file = Path(
                    self._dataDir.joinpath("klines")
                    .joinpath(symbol)
                    .joinpath(
                        "klines_{}.csv".format(
                            KlineInterval.getByUnit(self._interval, "m")
                        )
                    )
                )
                self._write_to_csv(data_file, listData)

                if latestRecords > 0:
                    nextEndTime = (
                        # -1 不和close时间戳相同,避免重新拉取重复数据
                        listData[0][0]
                        - 1
                    )

                    logger.debug(
                        "3、下次结束时间 %s %s"
                        % (TimeTools.format_timestamp(nextEndTime), nextEndTime)
                    )

                    if self._hisSwitch == 0 or nextEndTime <= self._hisDateTime:
                        break
                else:
                    logger.debug("4、结束...")

                # time.sleep(0.1)
            records = latestRecords + records
            logger.info("5、{} 抓取数据 {} 条记录...".format(symbol, records))
            logger.debug("{} symbol --------------------------------- ".format(symbol))
            # print(now + f"------ collect, {self._jobId} -- {records} done!")

    # def taskDetail(taskName: str):
    #     currTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #     logger.debug(f"{taskName}-->", "currTime:", currTime)
