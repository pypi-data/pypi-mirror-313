from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, composite

from app.user.domain.vo.location import Location
from core.db import Base
from core.db.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    nickname: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    is_admin: Mapped[bool] = mapped_column(Integer, default=True, nullable=False)

    # print(f"--------- is_admin:{is_admin.column.} -----------")
    # is_admin: Mapped[bool] = mapped_column(default=False)
    location: Mapped[Location] = composite(mapped_column("lat"), mapped_column("lng"))

    @classmethod
    def create(
        cls, *, email: str, password: str, nickname: str, location: Location
    ) -> "User":
        return cls(
            email=email,
            password=password,
            nickname=nickname,
            is_admin=False,
            location=location,
        )


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="USER ID")
    email: str = Field(..., title="Email")
    nickname: str = Field(..., title="Nickname")
    # is_admin: bool = Field(..., title="is_admin")
