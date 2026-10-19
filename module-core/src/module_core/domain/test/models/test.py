from sqlalchemy import String, Text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from module_core.common.config.database import Base, BaseTimeEntity

# *
# Test 도메인의 데이터베이스 테이블 매핑 엔티티 클래스입니다.
# *
class Test(Base, BaseTimeEntity):
    __tablename__ = "test"

    # 기본키 (JPA의 @Id @GeneratedValue(strategy = GenerationType.IDENTITY) 역할)
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, comment="고유 마스터 식별자 ID")
    # 문자열 컬럼 (JPA의 @Column(nullable = false, length = 255) 역할)
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="테스트 제목")
    # 대용량 텍스트 컬럼 (JPA의 @Lob 혹은 @Column(columnDefinition = "TEXT") 역할)
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="테스트 상세 본문 내용")
    