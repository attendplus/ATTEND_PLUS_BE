from typing import TYPE_CHECKING
from datetime import date, datetime

from sqlalchemy import BigInteger, ForeignKey, SmallInteger, DateTime, String, Boolean, Date, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from module_core.common.config.database import Base, BaseTimeEntity

if TYPE_CHECKING:
    from module_core.entities.user.user import User
    from module_core.entities.school.school_class import SchoolClass
    from module_core.entities.attendance.attendance_history import AttendanceHistory
    from module_core.entities.notification.notification import Notification

from module_core.entities.attendance.enums import Status, Method, ReasonType

class Attendance(Base, BaseTimeEntity):
    __tablename__ = "attendance"

    # Attendance ID
    att_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment="출결 ID")
    
    cls_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("school_class.cls_id"), nullable=False, comment="학급 ID")
    us_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.us_id"), nullable=False, comment="학생 ID")
    teacher_us_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("users.us_id"), nullable=True, comment="수동처리 교사 ID")

    att_date: Mapped[date] = mapped_column(Date, nullable=False, comment="날짜")
    per_no: Mapped[int] = mapped_column(SmallInteger, nullable=False, comment="교시")
    att_status: Mapped[Status] = mapped_column(SQLEnum(Status, name="att_status_enum"), nullable=False, comment="출석 상태 구분")
    att_method: Mapped[Method] = mapped_column(SQLEnum(Method, name="att_method_enum"), nullable=False, comment="GPS/QR 구분")
    att_is_confirmed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="확인 완료 여부")
    att_checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="실제 체크 시각")
    att_reason_type: Mapped[ReasonType] = mapped_column(SQLEnum(ReasonType, name="att_reason_type_enum"), nullable=True, comment="질병/무단/기타")
    att_reason: Mapped[str | None] = mapped_column(String, nullable=True, comment="사유")

    # 연관관계 - 역참조
    school_class: Mapped["SchoolClass"] = relationship(back_populates="attendance")
    student_user: Mapped["User"] = relationship(back_populates="attendance")
    teacher_user: Mapped["User"] = relationship(back_populates="attendance")

    # 참조
    history: Mapped[list["AttendanceHistory"]] = relationship(back_populates="attendance", cascade="all, delete-orphan") # 출결 엔티티 목록
    notifcation: Mapped[list["Notification"]] = relationship(back_populates="attendance", cascade="all, delete-orphan") # 알림 엔티티 목록
