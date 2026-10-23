from typing import TYPE_CHECKING

from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from module_core.common.config.database import Base, BaseTimeEntity

if TYPE_CHECKING:
    from module_core.entities.school.school import School
    from module_core.entities.timetable.personal_timetable import PersonalTimetable

class Classroom(Base, BaseTimeEntity):
    __tablename__ = "classroom"

    clr_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment="교실 ID")
    sc_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("school.sc_id"), nullable=False, comment="학교 ID")

    clr_name: Mapped[str] = mapped_column(String(50), nullable=False, comment="이름")
    clr_floor: Mapped[str] = mapped_column(String(100), nullable=False, comment="층")

    # 연관관계 - 역참조
    school: Mapped[School] = relationship(back_populates="classroom")

    # 참조
    personal_timetable: Mapped[list["PersonalTimetable"]] = relationship(back_populates="classroom") # 이동시간표 엔티티 목록
    