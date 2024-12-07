from app.openfund.domain.usecase.collect_usecase import CollectUseCase

from core.openfund.openfund import openfund as op
from core.openfund.log_tools import logger
from core.openfund.base_collector import Collector

from core.openfund.tradingClient.binance.binance_spot import BinanceSpotClient
from core.openfund.enums import KlineInterval


# from core.helpers.token import (
#     TokenHelper,
#     DecodeTokenException as JwtDecodeTokenException,
#     ExpiredTokenException as JwtExpiredTokenException,
# )


class CollectService(CollectUseCase):
    def __init__(self, *, collector: Collector) -> None:
        super().__init__()
        self._collector = collector

    async def collect(self) -> None:
        # print(f"---------  Hello CollectService {id(openfund)}--------")
        # print("")
        logger.debug(f"--------- CollectService.collect --------")
        time = BinanceSpotClient().get_time()
        logger.debug(f"--------- time = {time} --------")
        code = self._collector.start(interval=KlineInterval.KLINE_INTERVAL_1MINUTE)
        logger.debug(f"--------- code = {code} --------")
        # account = BinanceSpotTools().get_account()
        # logger.debug(
        #     f"--------- account.makerCommission = {account["makerCommission"]} --------"

        # try:
        #     TokenHelper.decode(token=token)
        # except (JwtDecodeTokenException, JwtExpiredTokenException):
        #     raise DecodeTokenException

    # async def create_refresh_token(
    #     self,
    #     token: str,
    #     refresh_token: str,
    # ) -> RefreshTokenResponseDTO:
    #     decoede_created_token = TokenHelper.decode(token=token)
    #     decoded_refresh_token = TokenHelper.decode(token=refresh_token)
    #     if decoded_refresh_token.get("sub") != "refresh":
    #         raise DecodeTokenException

    #     return RefreshTokenResponseDTO(
    #         token=TokenHelper.encode(
    #             payload={"user_id": decoede_created_token.get("user_id")}
    #         ),
    #         refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
    #     )
