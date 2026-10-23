from typing import TYPE_CHECKING
from datetime import date

from sqlalchemy import BigInteger, ForeignKey, SmallInteger, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from module_core.common.config.database import Base, BaseTimeEntity

if TYPE_CHECKING:
    from module_core.entities.user.user import User
    from module_core.entities.school.subjects import Subject
    from module_core.entities.classroom.classroom import Classroom

class PersonalTimetable(Base, BaseTimeEntity):
    __tablename__ = "personal_timetable"

    # Personal Timetable ID
    pt_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment="이동수업 ID")
    
    us_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.us_id"), nullable=False, comment="사용자(학생) ID")
    teacher_us_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("users.us_id"), nullable=True, comment="사용자(교사) ID")
    clr_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("classroom.clr_id"), nullable=True, comment="교실 ID")
    sub_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("subjects.sub_id"), nullable=False, comment="과목 ID")

    tt_date: Mapped[date] = mapped_column(Date, nullable=False, comment="날짜")
    per_no: Mapped[date] = mapped_column(SmallInteger, nullable=False, comment="교시")
    pt_group_label: Mapped[str] = mapped_column(String(5), nullable=False, comment="알파벳")

    # 연관관계 - 역참조
    user: Mapped["User"] = relationship(back_populates="personal_timetable")
    teacher_user: Mapped["User"] = relationship(back_populates="personal_timetable")
    classroom: Mapped["Classroom"] = relationship(back_populates="personal_timetable")
    subject: Mapped["Subject"] = relationship(back_populates="personal_timetable")
    