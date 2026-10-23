from typing import TYPE_CHECKING
from datetime import datetime, date

from sqlalchemy import BigInteger, ForeignKey, DateTime, String, Date, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from module_core.common.config.database import Base, BaseTimeEntity

if TYPE_CHECKING:
    from module_core.entities.user.user import User
    from module_core.entities.attendance.attendance import Attendance

from module_core.entities.notification.enums import NotificationType

class Notification(Base, BaseTimeEntity):
    __tablename__ = "notification"

    # Notifcation ID
    noti_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment="알림 ID")
    
    att_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("attendance.att_id"), nullable=True, comment="출결 ID")
    us_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.us_id"), nullable=False, comment="학생 ID")

    noti_type: Mapped[NotificationType | None] = mapped_column(SQLEnum(NotificationType, name="noti_type_enum"), nullable=False, comment="유형")
    noti_ref_date: Mapped[date | None] = mapped_column(Date, nullable=True, comment="날짜")
    noti_title: Mapped[str] = mapped_column(String(100), nullable=False, comment="제목")
    noti_body: Mapped[str | None] = mapped_column(String, nullable=True, comment="내용")
    noti_sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, comment="보낸 시각")
    noti_read_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, comment="읽은 시각")

    # 연관관계 - 역참조
    attendance: Mapped["Attendance"] = relationship(back_populates="notifcation")
    user: Mapped["User"] = relationship(back_populates="notifcation")
    