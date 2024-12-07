from __future__ import annotations

from core.openfund.base_tool import Tool as BaseTool
from core.openfund.enums import BINANCE_EXCHANGE

# from core.openfund.openfund import Openfund, openfund as of
# from core.openfund.log_tools import logger


# class SingletonMeta(type):
#     _instances = {}

#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             instance = super().__call__(*args, **kwargs)
#             cls._instances[cls] = instance
#         return cls._instances[cls]


# class BinanceUMFuturesClient(BaseTool, metaclass=SingletonMeta):
class BinanceUMFuturesClient(BaseTool):
    def __init__(self) -> None:
        super().__init__(tokenName=BINANCE_EXCHANGE)

    def time(self):
        return self.umclient.time()

    def ping(self):
        return self.umclient.ping()

    def klines(self, symbol: str, interval: str = "1m", **kwargs):
        return self.umclient.klines(symbol=symbol, interval=interval, **kwargs)
