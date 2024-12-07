from __future__ import annotations

import os

from pathlib import Path
from typing import TYPE_CHECKING

from platformdirs import user_cache_path
from platformdirs import user_config_path
from platformdirs import user_data_path
from platformdirs import user_log_path
from apscheduler.schedulers.base import BaseScheduler

from .enums import KlineInterval, APP_NAME
from .scheduler import OpenfundScheduler

from .factory import poetry

if TYPE_CHECKING:
    from poetry.poetry import Poetry

_APP_NAME = APP_NAME


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Openfund(metaclass=SingletonMeta):
    def __init__(self) -> None:
        pass
        # if self._poetry is None:

        # self._scheduler = scheduler
        # if self._scheduler is None:
        #     self._scheduler = OpenfundScheduler().scheduler

    @property
    def dataDir(self) -> Path:
        # openfund_home = os.getenv("OPENFUND_HOME")
        # if openfund_home:
        #     return Path(openfund_home).expanduser()
        return Path(
            os.getenv("OPENFUND_DATA_DIR")
            or user_data_path(_APP_NAME, appauthor=False, roaming=True)
        ).joinpath("data")

    @property
    def cacheDir(self) -> Path:
        return Path(
            os.getenv("OPENFUND_CACHE_DIR")
            or user_cache_path(_APP_NAME, appauthor=False)
        )

    @property
    def configDir(self) -> Path:

        return Path(
            os.getenv("OPENFUND_CONFIG_DIR")
            or user_config_path(_APP_NAME, appauthor=False, roaming=True)
        ).joinpath("config")

    @property
    def logDir(self) -> Path:

        return Path(
            os.getenv("OPENFUND_LOG_DIR")
            or user_log_path(
                _APP_NAME,
                appauthor=False,
                ensure_exists=True,
            )
        )

    @property
    def poetry(self) -> Poetry:
        return poetry

    # @property
    # def scheduler(self) -> BaseScheduler:
    #     return self._scheduler

    def getConfig(self, key: str) -> str:
        return poetry.config.get(key)


openfund = Openfund()
