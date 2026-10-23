from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from module_core.common.config.database import Base, BaseTimeEntity

class S3File(Base, BaseTimeEntity):
    __tablename__ = "s3_file"

    # S3 File ID
    sf_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, comment="S3 파일 ID")

    sf_original_name: Mapped[str] = mapped_column(String, nullable=False, comment="원본명")
    sf_name: Mapped[str] = mapped_column(String, nullable=False, comment="파일명")
    sf_url: Mapped[str] = mapped_column(String, nullable=False, comment="S3 URL")
    sf_content_type: Mapped[str] = mapped_column(String, nullable=True, comment="Body 유형")
    sf_size: Mapped[int] = mapped_column(BigInteger, nullable=True, comment="크기")
    