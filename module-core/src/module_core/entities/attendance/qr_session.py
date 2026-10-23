from typing import TYPE_CHECKING
from datetime import datetime, date

from sqlalchemy import BigInteger, ForeignKey, SmallInteger, DateTime, Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from module_core.common.config.database import Base, BaseTimeEntity

if TYPE_CHECKING:
    from module_core.entities.user.user import User
    from module_core.entities.school.school_class import SchoolClass

class QRSession(Base, BaseTimeEntity):
    __tablename__ = "qr_session"

    # QR Session ID
    qr_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment="QR 세션 ID")
    
    cls_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("school_class.cls_id"), nullable=False, comment="학급 ID")
    teacher_us_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("users.us_id"), nullable=True, comment="사용자(교사) ID")

    qr_date: Mapped[date] = mapped_column(Date, nullable=False, comment="날짜")
    per_no: Mapped[int] = mapped_column(SmallInteger, nullable=False, comment="교시")
    qr_code: Mapped[str] = mapped_column(String, nullable=False, comment="QR 코드")
    qr_expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, comment="만료 시각")
    qr_revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="폐기 시각")

    # 연관관계 - 역참조
    school_class: Mapped["SchoolClass"] = relationship(back_populates="qr_session")
    user: Mapped["User"] = relationship(back_populates="qr_session")
    