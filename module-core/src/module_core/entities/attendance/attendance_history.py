from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.dialects import postgresql
from sqlalchemy import BigInteger, ForeignKey, DateTime, String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from module_core.common.config.database import Base, BaseTimeEntity

if TYPE_CHECKING:
    from module_core.entities.user.user import User
    from module_core.entities.attendance.attendance import Attendance

from module_core.entities.attendance.enums import Status

class AttendanceHistory(Base, BaseTimeEntity):
    __tablename__ = "attendance_history"

    # Attendance History ID
    ah_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment="수동처리 출결 기록 ID")
    
    att_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("attendance.att_id"), nullable=False, comment="출결 ID")
    us_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.us_id"), nullable=False, comment="학생 ID")

    ah_old_status: Mapped[Status | None] = mapped_column(postgresql.ENUM(Status, name="att_status_enum", create_type=False), nullable=True, comment="기존 출결 상태")
    ah_new_status: Mapped[Status] = mapped_column(postgresql.ENUM(Status, name="att_status_enum", create_type=False), nullable=False, comment="새로운 출결 상태")
    ah_reason: Mapped[str] = mapped_column(String, nullable=False, comment="사유")
    ah_changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, comment="변경일")

    # 연관관계 - 역참조
    attendance: Mapped["Attendance"] = relationship(back_populates="attendance_history")
    user: Mapped["User"] = relationship(back_populates="attendance_history")
    