from typing import TYPE_CHECKING

from sqlalchemy import String, BigInteger, ForeignKey, SmallInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from module_core.common.config.database import Base, BaseTimeEntity

if TYPE_CHECKING:
    from module_core.entities.school.school import School
    from module_core.entities.user.user import User
    from module_core.entities.attendance.attendance import Attendance
    from module_core.entities.classroom.classroom_member import ClassroomMember
    from module_core.entities.timetable.timetable import Timetable
    from module_core.entities.attendance.qr_session import QRSession
    from module_core.entities.schedule.schedule import Schedule

class SchoolClass(Base, BaseTimeEntity):
    __tablename__ = "school_class"

    # Class ID
    cls_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment="학급 ID")

    sc_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("school.sc_id"), nullable=False, comment="학교 ID")
    teacher_us_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("users.us_id"), nullable=True, comment="사용자(교사) ID")

    cls_school_year: Mapped[int] = mapped_column(SmallInteger, nullable=False, comment="학년도")
    cls_grade: Mapped[int] = mapped_column(SmallInteger, nullable=False, comment="학년")
    cls_number: Mapped[int] = mapped_column(SmallInteger, nullable=False, comment="학급")
    cls_is_activate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, comment="활성화 여부")
    cls_description: Mapped[str | None] = mapped_column(String, nullable=True, comment="설명")
    cls_access_code: Mapped[str] = mapped_column(String, nullable=False, comment="고유인증코드")

    # 연관관계 - 역참조
    school: Mapped["School"] = relationship(back_populates="school_class") # 학교 엔티티
    user: Mapped["User"] = relationship(back_populates="school_class") # 사용자(교사) 엔티티

    # 참조
    attendance: Mapped[list["Attendance"]] = relationship(back_populates="school_class") # 출결 엔티티 목록
    classroom_member: Mapped[list["ClassroomMember"]] = relationship(back_populates="school_class") # 학급 회원 엔티티 목록
    timetable: Mapped[list["Timetable"]] = relationship(back_populates="school_class", cascade="all, delete-orphan") # 시간표 엔티티 목록
    qr_session: Mapped[list["QRSession"]] = relationship(back_populates="school_class", cascade="all, delete-orphan") # QR 세션 엔티티 목록
    schedule: Mapped[list["Schedule"]] = relationship(back_populates="school_class", cascade="all, delete-orphan") # 일정 엔티티 목록
    