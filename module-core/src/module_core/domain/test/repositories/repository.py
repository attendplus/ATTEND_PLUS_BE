# Repository Layer
from module_core.domain.test.models.test import Test
from module_core.common.config.database import BaseRepository

# *
# Repository는 Spring Boot의 Repository 형식을 그대로 따라갑니다.
# *
class TestRepository(BaseRepository[Test]):
    def __init__(self):
        super().__init__(Test)

# 싱글톤 객체 생성
test_repository = TestRepository()
    