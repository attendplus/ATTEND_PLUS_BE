from typing import TYPE_CHECKING
from datetime import time

from sqlalchemy import BigInteger, ForeignKey, SmallInteger, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from module_core.common.config.database import Base, BaseTimeEntity

if TYPE_CHECKING:
    from module_core.entities.school.school import School

class Period(Base, BaseTimeEntity):
    __tablename__ = "school_period"

    sp_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment="교시 ID")
    sc_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("school.sc_id"), nullable=False, comment="학교 ID")

    per_no: Mapped[str] = mapped_column(SmallInteger, nullable=False, comment="교시")
    per_start: Mapped[time] = mapped_column(Time, nullable=False, comment="시작 시각")
    per_end: Mapped[time] = mapped_column(Time, nullable=False, comment="종료 시각")

    # 연관관계 - 역참조
    school: Mapped["School"] = relationship(back_populates="school_period")
    