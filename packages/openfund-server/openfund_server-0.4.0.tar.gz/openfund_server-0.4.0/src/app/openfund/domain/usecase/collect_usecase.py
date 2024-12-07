from abc import ABC, abstractmethod

# from app.auth.application.dto import RefreshTokenResponseDTO


class CollectUseCase(ABC):
    @abstractmethod
    async def collect(self) -> None:
        """collect"""

    # @abstractmethod
    # async def create_refresh_token(
    #     self,
    #     token: str,
    #     refresh_token: str,
    # ) -> RefreshTokenResponseDTO:
    #     """Create refresh token"""
