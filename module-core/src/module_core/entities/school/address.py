from typing import TYPE_CHECKING

from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from module_core.common.config.database import Base, BaseTimeEntity

if TYPE_CHECKING:
    from module_core.entities.school.school import School

class Address(Base, BaseTimeEntity):
    __tablename__ = "address"

    addr_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment="주소 ID")
    sc_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("school.sc_id"), nullable=False, comment="학교 ID")

    do: Mapped[str] = mapped_column(String(20), nullable=False, comment="도")
    city: Mapped[str] = mapped_column(String(20), nullable=False, comment="시")
    gun_gu: Mapped[str] = mapped_column(String(20), nullable=False, comment="군/구")
    eup_myeon: Mapped[str] = mapped_column(String(20), nullable=False, comment="읍/면")
    dong: Mapped[str] = mapped_column(String(20), nullable=False, comment="동")
    road_name: Mapped[str] = mapped_column(String(20), nullable=False, comment="도로명")
    building_number: Mapped[str] = mapped_column(String(20), nullable=False, comment="건물번호")

    # 연관관계 - 역참조
    school: Mapped["School"] = relationship(back_populates="address")
    