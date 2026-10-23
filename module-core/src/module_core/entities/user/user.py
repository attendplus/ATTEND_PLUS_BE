from typing import TYPE_CHECKING

from sqlalchemy import String, BigInteger, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from module_core.common.config.database import Base, BaseTimeEntity

if TYPE_CHECKING:
  from module_core.entities.school.school import School
  from module_core.entities.user.device import Device
  from module_core.entities.school.school_class import SchoolClass
  from module_core.entities.classroom.classroom_member import ClassroomMember
  from module_core.entities.attendance.attendance import Attendance
  from module_core.entities.attendance.attendance_history import AttendanceHistory
  from module_core.entities.notification.notification import Notification
  from module_core.entities.timetable.timetable import Timetable
  from module_core.entities.timetable.personal_timetable import PersonalTimetable
  from module_core.entities.attendance.qr_session import QRSession
  from module_core.entities.schedule.schedule import Schedule
  from module_core.entities.schedule.schedule_target import ScheduleTarget

from module_core.entities.user.enums import GenderEnum, RoleEnum, EmploymentStatusEnum

class User(Base, BaseTimeEntity):
    __tablename__ = "users"

    # User ID
    us_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, comment="사용자 ID")
    
    sc_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("school.sc_id"), comment="학교 ID")

    us_name: Mapped[str] = mapped_column(String(20), nullable=False, comment="이름(실명)")
    us_email: Mapped[str] = mapped_column(String(100), nullable=False, comment="이메일")
    us_password: Mapped[str] = mapped_column(String, nullable=False, comment="비밀번호")
    us_gender: Mapped[GenderEnum] = mapped_column(SQLEnum(GenderEnum, name="us_gender_enum"), nullable=False, comment="성별")
    us_is_foreign: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="외국인 여부")
    us_profile_sf_url: Mapped[str | None] = mapped_column(String, nullable=True, comment="프로필 S3 URL")
    us_role: Mapped[RoleEnum] = mapped_column(SQLEnum(RoleEnum, name="us_role_enum"), nullable=False, comment="권한")
    us_activate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, comment="활성화 여부")
    us_deactivate_reason: Mapped[str | None] = mapped_column(String, nullable=True, comment="비활성화 사유")
    us_employment_status: Mapped[EmploymentStatusEnum] = mapped_column(SQLEnum(EmploymentStatusEnum, name="us_employment_status_enum"), nullable=False, comment="교사 재직 상태")
    us_must_change_password: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="임시 비번 계정")
    us_alarm_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, comment="알림 수신")
    us_rotational_timetable_file_url: Mapped[str | None] = mapped_column(String, nullable=True, comment="이동수업 시간표 파일 URL")

    # 연관관계 - 역참조
    school: Mapped["School"] = relationship(back_populates="users") # 학교 엔티티

    # 참조
    device: Mapped["Device"] = relationship(back_populates="users", cascade="all, delete-orphan") # 기기 엔티티
    school_class: Mapped["SchoolClass"] = relationship(back_populates="users", cascade="all, delete-orphan") # 학급 엔티티
    classroom_member: Mapped[list["ClassroomMember"]] = relationship(back_populates="users", cascade="all, delete-orphan") # 학급 회원 엔티티
    attendance: Mapped[list["Attendance"]] = relationship(back_populates="users", cascade="all, delete-orphan") # 출결 엔티티 목록
    attendance_history: Mapped[list["AttendanceHistory"]] = relationship(back_populates="users", cascade="all, delete-orphan") # 수동처리 출결 기록 엔티티 목록
    notifcation: Mapped[list["Notification"]] = relationship(back_populates="users", cascade="all, delete-orphan") # 수동처리 출결 기록 엔티티 목록
    timetable: Mapped[list["Timetable"]] = relationship(back_populates="users", cascade="all, delete-orphan") # 시간표 엔티티 목록
    personal_timetable: Mapped[list["PersonalTimetable"]] = relationship(back_populates="users") # 이동시간표 엔티티 목록
    qr_session: Mapped[list["QRSession"]] = relationship(back_populates="users") # QR 세션 엔티티 목록
    schedule: Mapped[list["Schedule"]] = relationship(back_populates="users", cascade="all, delete-orphan") # 일정 엔티티 목록
    schedule_target: Mapped[list["ScheduleTarget"]] = relationship(back_populates="users", cascade="all, delete-orphan") # 일정 학생 엔티티 목록
