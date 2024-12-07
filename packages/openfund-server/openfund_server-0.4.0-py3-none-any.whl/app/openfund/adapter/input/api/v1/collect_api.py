from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response
from app.container import Container
from app.openfund.adapter.input.api.v1.request import (
    AddJobRequest,
)

# from app.auth.adapter.input.api.v1.response import RefreshTokenResponse
from app.openfund.domain.usecase.collect_usecase import CollectUseCase


collect_router = APIRouter()


# @auth_router.post(
#     "/refresh",
#     response_model=RefreshTokenResponse,
# )
# @inject
# async def refresh_token(
#     request: RefreshTokenRequest,
#     usecase: JwtUseCase = Depends(Provide[Container.jwt_service]),
# ):
#     token = await usecase.create_refresh_token(
#         token=request.token, refresh_token=request.refresh_token
#     )
#     return {"token": token.token, "refresh_token": token.refresh_token}


@collect_router.post("/add")
@inject
async def addJob(
    request: AddJobRequest,
    usecase: CollectUseCase = Depends(Provide[Container.collect_service]),
):
    # await usecase.collect(token=request.token)
    await usecase.collect()
    return Response(status_code=200)
