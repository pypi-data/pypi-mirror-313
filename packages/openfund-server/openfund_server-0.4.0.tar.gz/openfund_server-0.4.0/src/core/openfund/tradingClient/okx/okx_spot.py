from __future__ import annotations

from core.openfund.base_tool import Tool as BaseTool
from core.openfund.openfund import openfund as op
from core.openfund.log_tools import logger


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class OKXSpotTools(BaseTool, metaclass=SingletonMeta):
    def __init__(
        self,
    ) -> None:
        super().__init__("okx")

    async def get_time(self):
        times = await self.client.time()
        return times

    def get_account(self):
        return self.client.account()

    def get_klines(self, symbol: str, interval: str, **kwargs):
        return self.client.klines(symbol=symbol, interval=interval, **kwargs)
