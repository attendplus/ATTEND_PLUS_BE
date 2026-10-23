from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from module_core.common.config.database import Base, BaseTimeEntity

if TYPE_CHECKING:
    from module_core.entities.user.user import User
    from module_core.entities.schedule.schedule import Schedule

class ScheduleTarget(Base, BaseTimeEntity):
    __tablename__ = "schedule_target"

    sct_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment="일정 대상 ID")
    sch_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("schedule.sch_id"), nullable=False, comment="일정 ID")
    us_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.us_id"), nullable=False, comment="사용자(학생) ID")

    # 연관관계 - 역참조
    schedule: Mapped["Schedule"] = relationship(back_populates="schedule_target")
    user: Mapped["User"] = relationship(back_populates="schedule_target")
    