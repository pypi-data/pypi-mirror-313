from pydantic import BaseModel, Field


class AddJobRequest(BaseModel):
    jobId: str = Field(..., description="jobId")
    interval: int = Field(..., description="interval")
    unit: str = Field(..., description="unit")


# class RefreshTokenRequest(BaseModel):
#     token: str = Field(..., description="Token")
#     refresh_token: str = Field(..., description="Refresh token")


# class VerifyTokenRequest(BaseModel):
#     token: str = Field(..., description="Token")
