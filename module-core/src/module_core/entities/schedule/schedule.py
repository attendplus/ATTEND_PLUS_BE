from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, SmallInteger, String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from module_core.common.config.database import Base, BaseTimeEntity

if TYPE_CHECKING:
    from module_core.entities.user.user import User
    from module_core.entities.school.school_class import SchoolClass
    from module_core.entities.school.school import School
    from module_core.entities.schedule.schedule_period import SchedulePeriod
    from module_core.entities.schedule.schedule_target import ScheduleTarget

from module_core.entities.schedule.enums import Scope

class Schedule(Base, BaseTimeEntity):
    __tablename__ = "schedule"

    # Schedule ID
    sch_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment="일정 ID")
    
    sc_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("school.sc_id"), nullable=False, comment="학교 ID")
    cls_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("school_class.cls_id"), nullable=False, comment="학급 ID")
    teacher_us_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("users.us_id"), nullable=False, comment="사용자 ID")

    sch_title: Mapped[str] = mapped_column(String(100), nullable=False, comment="일정 제목")
    sch_reason: Mapped[str] = mapped_column(String, nullable=True, comment="일정 사유")
    sch_skip_attendance: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, comment="출결 여부")
    sch_note: Mapped[str | None] = mapped_column(String, nullable=True, comment="참고 사항")
    sch_scope: Mapped[Scope] = mapped_column(SQLEnum(Scope, name="sch_scope_enum"), nullable=False, comment="학교/학년/학급/학생 구분")
    sch_grade: Mapped[int | None] = mapped_column(SmallInteger, nullable=True, comment="학년")

    # 연관관계 - 역참조
    school: Mapped["School"] = relationship(back_populates="schedule")
    school_class: Mapped["SchoolClass"] = relationship(back_populates="schedule")
    user: Mapped["User"] = relationship(back_populates="schedule")

    # 참조
    schedule_period: Mapped[list["SchedulePeriod"]] = relationship(back_populates="schedule", cascade="all, delete-orphan") # 일정 교시 엔티티 목록
    schedule_target: Mapped[list["ScheduleTarget"]] = relationship(back_populates="schedule", cascade="all, delete-orphan") # 일정 학생 엔티티 목록
    