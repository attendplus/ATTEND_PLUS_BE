from typing import TYPE_CHECKING
from datetime import date

from sqlalchemy import BigInteger, ForeignKey, SmallInteger, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from module_core.common.config.database import Base, BaseTimeEntity

if TYPE_CHECKING:
    from module_core.entities.user.user import User
    from module_core.entities.school.school import School
    from module_core.entities.school.school_class import SchoolClass

class Timetable(Base, BaseTimeEntity):
    __tablename__ = "timetable"

    # TimeTable ID
    tt_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment="시간표 ID")
    
    sc_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("school.sc_id"), nullable=False, comment="학교 ID")
    cls_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("school_class.cls_id"), nullable=True, comment="학급 ID")
    us_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("users.us_id"), nullable=True, comment="사용자(교사) ID")

    tt_date: Mapped[date] = mapped_column(Date, nullable=False, comment="날짜")
    per_no: Mapped[int] = mapped_column(SmallInteger, nullable=False, comment="교시")
    tt_is_changed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="수정 여부")

    # 연관관계 - 역참조
    school: Mapped["School"] = relationship(back_populates="timetable")
    school_class: Mapped["SchoolClass"] = relationship(back_populates="timetable")
    user: Mapped["User"] = relationship(back_populates="timetable")
    