from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey, Integer, SmallInteger, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from module_core.common.config.database import Base, BaseTimeEntity

if TYPE_CHECKING:
    from module_core.entities.user.user import User
    from module_core.entities.school.school_class import SchoolClass

from module_core.entities.classroom.enums import Status

class ClassroomMember(Base, BaseTimeEntity):
    __tablename__ = "classroom_member"

    # Classroom Member ID
    cm_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment="학급 회원 ID")
    
    cls_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("school_class.cls_id"), nullable=False, comment="학급 ID")
    us_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.us_id"), nullable=False, comment="사용자 ID")

    cm_student_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="학번")
    cm_number: Mapped[int] = mapped_column(SmallInteger, nullable=False, comment="번호")
    cm_status: Mapped[Status] = mapped_column(SQLEnum(Status, name="cm_status_enum"), nullable=False, comment="상태")
    cm_requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, comment="요청일")
    cm_decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="가입일")

    # 연관관계 - 역참조
    school_class: Mapped["SchoolClass"] = relationship(back_populates="classroom_member")
    user: Mapped["User"] = relationship(back_populates="classroom_member")
    