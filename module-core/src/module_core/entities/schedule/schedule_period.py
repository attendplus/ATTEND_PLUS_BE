from typing import TYPE_CHECKING
from datetime import date

from sqlalchemy import BigInteger, ForeignKey, SmallInteger, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from module_core.common.config.database import Base, BaseTimeEntity

if TYPE_CHECKING:
    from module_core.entities.schedule.schedule import Schedule

class SchedulePeriod(Base, BaseTimeEntity):
    __tablename__ = "schedule_period"

    # Schedule Period ID
    sp_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment="일정 교시 ID")

    sch_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("schedule.sch_id"), nullable=False, comment="일정 ID")

    sp_date: Mapped[date] = mapped_column(Date, nullable=False, comment="날짜")
    per_no: Mapped[int | None] = mapped_column(SmallInteger, nullable=True, comment="교시")

    # 연관관계 - 역참조
    schedule: Mapped["Schedule"] = relationship(back_populates="schedule_period")

    