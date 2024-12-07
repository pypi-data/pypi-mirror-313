from __future__ import annotations

from pathlib import Path

from typing import TYPE_CHECKING

from binance.spot import Spot as Client
from binance.um_futures import UMFutures as UMClient

from .enums import BINANCE_EXCHANGE
from .openfund import Openfund, openfund as op
from .log_tools import logger

# from .factory import poetry


class Tool:
    def __init__(
        self, openfund: Openfund | None = None, tokenName: str = BINANCE_EXCHANGE
    ) -> None:
        self._openfund: Openfund = openfund
        if self._openfund is None:
            self._openfund = op
            # self._openfund = Factory().init_openfund()
        # self._poetry = poetry
        self._tokenName = tokenName
        # self._password_manager = Authenticator(
        #     self._openfund._poetry.config
        # )._password_manager

        self._client = None
        self._umclient = None

    @property
    def api_key(self) -> str:
        return op.getConfig(f"http-basic.{ self._tokenName}.username")
        # return self._openfund.config.get(f"http-basic.{ self._toolname}.username")
        # return self._password_manager.get_http_auth(self._toolname).get("username")

    @property
    def apk_secret(self) -> str:
        return op.getConfig(f"http-basic.{ self._tokenName}.password")
        # return self._poetry.config.get(f"http-basic.{ self._toolname}.password")
        # return self._password_manager.get_http_auth(self._toolname).get("password")

    @property
    def client(self) -> Client:
        if self._client is None:
            self._client = Client(self.api_key, self.apk_secret)
        return self._client

    @property
    def umclient(self) -> UMClient:
        if self._umclient is None:
            self._umclient = UMClient(self.api_key, self.apk_secret)
        return self._umclient
