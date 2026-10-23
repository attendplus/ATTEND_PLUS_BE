from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from module_core.common.config.database import Base, BaseTimeEntity
from module_core.entities.school.school import School

if TYPE_CHECKING:
    from module_core.entities.timetable.personal_timetable import PersonalTimetable

class Subject(Base, BaseTimeEntity):
    __tablename__ = "subjects"

    # Subjects ID
    sub_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment="과목 ID")

    sc_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("school.sc_id"), nullable=True, comment="학교 ID")

    sub_name: Mapped[str] = mapped_column(String(50), nullable=False, comment="과목 이름")
    sub_alphabet: Mapped[str | None] = mapped_column(String(5), nullable=True, comment="과목 알파벳")

    # 연관관계 - 역참조
    school: Mapped["School"] = relationship(back_populates="subjects")

    # 참조
    personal_timetable: Mapped[list["PersonalTimetable"]] = relationship(back_populates="subjects", cascade="all, delete-orphan") # 이동시간표 엔티티 목록
    