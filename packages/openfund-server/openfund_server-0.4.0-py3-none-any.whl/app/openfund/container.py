from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from core.openfund.tradingClient.binance.binance_futures import BinanceUMFuturesClient

from app.openfund.application.service.collect_service import CollectService
from app.openfund.domain.entity.um_futures_collector import KLinesCollectorEntity


class OpenfundContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=["app"])

    um_futures_client = Factory(BinanceUMFuturesClient)

    klines_collector = Factory(KLinesCollectorEntity, client=um_futures_client)

    # collect_service = Factory(CollectService, collector=klines_collector)
