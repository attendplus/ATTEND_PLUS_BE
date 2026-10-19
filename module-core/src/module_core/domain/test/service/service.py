# Service Layer
from module_core.domain.test.models.test import Test
from module_core.domain.test.router.request.schema import CreateTestRequest, UpdateTestRequest
from module_core.domain.test.router.response.schema import DetailTestResponse, ListDetailTestResponse
from module_core.domain.test.repositories.repository import test_repository
from module_core.domain.test.service.base import AbstractTestService

from module_core.common.exception import GlobalException
from module_core.common.type import ErrorStatus
from module_core.common.config.database import transactional

# *
# 특정 도메인의 비즈니스 로직을 담당하는 서비스 클래스입니다.
# AbstractXXXService 추상 클래스를 상속받아 정의된 인터페이스를 규격에 맞게 구현합니다.
# *
class TestService(AbstractTestService):
    def __init__(self):
        self.repository = test_repository

    # *
    # @transactional 데코레이터는 Spring Boot의 @Transactional 어노테이션과 동일한 역할을 합니다.
    # 단순 조회 작업일 경우 read_only를 True로 설정하여 DB 세션만 획득하도록 설정해 주세요!
    # 반면 쓰기 작업일 경우, DB 세션 획득과 동시에 트랜잭션 관리가 이루어져야 하므로 read_only를 False로 설정하거나 비워두시면 됩니다. (기본값이 False로 지정되어 있습니다.)
    # *

    # 테스트 생성 메서드
    @transactional(read_only=False)
    async def create_test(self, request: CreateTestRequest):
        entity: Test = Test(**request.model_dump())
        await self.repository.save(entity=entity)

    # 특정 테스트 조회 메서드
    @transactional(read_only=True)
    async def get_test(self, id: int) -> DetailTestResponse:
        entity: Test = await self.repository.find_by_id(id)
    
        if entity is None:
            raise GlobalException(ErrorStatus.INVALID_PARAMETER)
        
        return DetailTestResponse(
            id=entity.id,
            title=entity.title,
            content=entity.content,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    # 테스트 목록 조회 메서드
    @transactional(read_only=True)
    async def get_test_list(self) -> ListDetailTestResponse:
        entities: list[Test] = await self.repository.find_all()
        test_list: list[DetailTestResponse] = [
            DetailTestResponse(
                id=entity.id,
                title=entity.title,
                content=entity.content,
                created_at=entity.created_at,
                updated_at=entity.updated_at
            )
            for entity in entities
        ]

        return ListDetailTestResponse(tests=test_list)

    # 특정 테스트 수정 메서드
    @transactional(read_only=False)
    async def update_test(self, id: int, request: UpdateTestRequest) -> DetailTestResponse:
        entity: Test = await self.repository.find_by_id(id)
        
        if entity is None:
            raise GlobalException(ErrorStatus.INVALID_PARAMETER)

        # 파라미터로 받은 ID가 유효한지 선검증한 후 필드를 변경하고 머지(Merge)
        entity.title, entity.content = request.title, request.content
        self.repository.save(entity)

        return DetailTestResponse(
            id=entity.id,
            title=entity.title,
            content=entity.content,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    # 특정 테스트 삭제 메서드
    @transactional(read_only=False)
    async def delete_test(self, id: int):
        entity: Test = await self.repository.find_by_id(id)

        if entity is None:
            raise GlobalException(ErrorStatus.INVALID_PARAMETER)

        await self.repository.delete(entity)

# 싱글톤 객체 생성
test_service = TestService()
