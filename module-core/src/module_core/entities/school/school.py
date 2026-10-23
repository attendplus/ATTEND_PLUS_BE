from typing import TYPE_CHECKING

from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from module_core.common.config.database import Base, BaseTimeEntity

if TYPE_CHECKING:
    from module_core.entities.school.address import Address
    from module_core.entities.school.period import Period
    from module_core.entities.user.user import User
    from module_core.entities.classroom.classroom import Classroom
    from module_core.entities.school.school_class import SchoolClass
    from module_core.entities.school.subjects import Subject
    from module_core.entities.timetable.timetable import Timetable
    from module_core.entities.schedule.schedule import Schedule

class School(Base, BaseTimeEntity):
    __tablename__ = "school"

    # School ID
    sc_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment="학교 ID")

    sc_name: Mapped[str] = mapped_column(String(50), nullable=False, comment="이름")
    sc_en_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="영어 이름")
    sc_type: Mapped[str] = mapped_column(String(20), nullable=False, comment="학교 유형")
    sc_founding_type: Mapped[str] = mapped_column(String(20), nullable=False, comment="설립 유형")
    sc_track: Mapped[str] = mapped_column(String(20), nullable=False, comment="계열")
    sc_coedu_type: Mapped[str] = mapped_column(String(20), nullable=False, comment="남녀공학 구분")
    sc_website: Mapped[str] = mapped_column(String, nullable=False, comment="웹사이트")
    sc_office_name: Mapped[str] = mapped_column(String(20), nullable=False, comment="시도교육청명")
    sc_office_code: Mapped[str] = mapped_column(String(20), nullable=False, comment="시도교육청코드")
    sc_phone_number: Mapped[str] = mapped_column(String(20), nullable=False, comment="전화번호")
    sc_fax_number: Mapped[str] = mapped_column(String(20), nullable=False, comment="팩스번호")
    sc_access_code: Mapped[str] = mapped_column(String(50), nullable=False, comment="고유인증코드")
    sc_layout_file_url: Mapped[str] = mapped_column(String, nullable=True, comment="교실 배치도 파일 URL")

    # 연관관계
    address: Mapped["Address"] = relationship(back_populates="school", uselist=False, cascade="all, delete-orphan") # 주소 엔티티
    period: Mapped[list["Period"]] = relationship(back_populates="school", cascade="all, delete-orphan") # 학교 교시 엔티티 목록
    users: Mapped[list["User"]] = relationship(back_populates="school", cascade="all, delete-orphan") # 사용자 엔티티 목록
    classroom: Mapped[list["Classroom"]] = relationship(back_populates="school", cascade="all, delete-orphan") # 교실 엔티티 목록
    school_class: Mapped[list["SchoolClass"]] = relationship(back_populates="school", cascade="all, delete-orphan") # 학급 엔티티 목록
    subjects: Mapped[list["Subject"]] = relationship(back_populates="school", cascade="all, delete-orphan") # 과목 엔티티 목록
    timetable: Mapped[list["Timetable"]] = relationship(back_populates="school", cascade="all, delete-orphan") # 시간표 엔티티 목록
    schedule: Mapped[list["Schedule"]] = relationship(back_populates="school", cascade="all, delete-orphan") # 일정 엔티티 목록
    