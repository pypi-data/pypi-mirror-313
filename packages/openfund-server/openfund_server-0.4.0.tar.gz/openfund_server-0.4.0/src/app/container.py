from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton
from core.openfund.tradingClient.binance.binance_futures import BinanceUMFuturesClient

from app.auth.application.service.jwt import JwtService
from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo
from app.user.application.service.user import UserService

from app.openfund.application.service.collect_service import CollectService
from app.openfund.container import OpenfundContainer


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["app"])

    user_repo = Singleton(UserSQLAlchemyRepo)
    user_repo_adapter = Factory(UserRepositoryAdapter, user_repo=user_repo)
    user_service = Factory(UserService, repository=user_repo_adapter)

    jwt_service = Factory(JwtService)

    # um_futures_client = Singleton(BinanceUMFuturesClient)

    # klines_collector = Factory(KLinesCollectorEntity, client=um_futures_client)

    collect_service = Factory(CollectService, collector=OpenfundContainer.klines_collector)
