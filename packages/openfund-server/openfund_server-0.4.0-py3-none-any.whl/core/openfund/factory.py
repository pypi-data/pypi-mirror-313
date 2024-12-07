from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from poetry.factory import Factory as BaseFactory

if TYPE_CHECKING:
    from poetry.poetry import Poetry


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Factory(BaseFactory, metaclass=SingletonMeta):
    def __init__(self) -> None:
        super().__init__()
        # self._init_log()
        self._poetry = None
        # self._file_handler = None
        # self._console_handler = None
        # self._openfund: Openfund = None

    @property
    def poetry(self) -> Poetry:
        if self._poetry is None:
            _cwd = Path.cwd()
            self._poetry = self.create_poetry(cwd=_cwd, with_groups=True)
        return self._poetry


poetry = Factory().poetry
#     fileHandler = FileHandler(log_file)
#     fileHandler.setFormatter(FileFormatter())
#     console_handler = logging.StreamHandler()
#     console_handler.setFormatter(FileFormatter())
#     # logging.basicConfig(
#     #     level=logging.DEBUG,
#     #     handlers=[console_handler, fileHandler],
#     # )
#     # logger.addHandler(fileHandler)
#     # logger.addHandler(console_handler)

#     self._file_handler = fileHandler
#     self._console_handler = console_handler


# from logging.handlers import TimedRotatingFileHandler


# class FileHandler(TimedRotatingFileHandler):
#     def __init__(
#         self,
#         filename,
#         when="midnight",
#         interval=1,
#         backupCount=7,
#         encoding=None,
#         delay=False,
#         utc=False,
#     ) -> None:
#         super().__init__(filename, when, interval, backupCount, encoding, delay, utc)


# class FileFormatter(logging.Formatter):

#     _format = "%(asctime)s - %(process)d | %(threadName)s | %(module)s.%(funcName)s:%(lineno)d - %(levelname)s -%(message)s"

#     _datefmt = "%Y-%m-%d-%H:%M:%S"  # 时间

#     def __init__(self, fmt=_format, datefmt=_datefmt, style="%") -> None:
#         super().__init__(fmt, datefmt, style)
