from sqlalchemy import BigInteger, DateTime, String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column

from module_core.common.config.database import Base, BaseTimeEntity

class EmailVerification(Base, BaseTimeEntity):
    __tablename__ = "email_verification"

    # Email Verification ID
    ev_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, comment="이메일 ID")

    ev_email: Mapped[str] = mapped_column(String, nullable=False, comment="이메일")
    ev_code_hash: Mapped[str] = mapped_column(String, nullable=False, comment="인증 코드")
    ev_attempts: Mapped[int] = mapped_column(SmallInteger, nullable=False, comment="틀린 입력 횟수")
    ev_expires_at: Mapped[str] = mapped_column(DateTime(timezone=True), nullable=False, comment="만료 시각")
    ev_verified_at: Mapped[int] = mapped_column(DateTime(timezone=True), nullable=True, comment="인증 성공 시각")
    