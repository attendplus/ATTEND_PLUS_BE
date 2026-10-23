from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey, Boolean, Enum as SQLEnum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from module_core.common.config.database import Base, BaseTimeEntity

if TYPE_CHECKING:
    from module_core.entities.user.user import User

from module_core.entities.user.enums import PlatformEnum

class Device(Base, BaseTimeEntity):
    __tablename__ = "device"

    dev_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment="기기 ID")
    us_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.us_id"), nullable=False, comment="사용자 ID")

    platform: Mapped[PlatformEnum] = mapped_column(SQLEnum(PlatformEnum, name="dev_platform_enum"), nullable=False, comment="플랫폼 OS")
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, comment="통신한 시각")
    is_notification: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="알림 권한")
    is_location: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="위치 권한")
    is_background_location: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="백그라운드 권한")
    is_camera: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="카메라 권한")

    # 연관관계 - 역참조
    user: Mapped["User"] = relationship(back_populates="device") # 기기
    