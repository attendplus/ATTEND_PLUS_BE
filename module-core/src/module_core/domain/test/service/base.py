from abc import ABC, abstractmethod

from module_core.domain.test.router.request.schema import CreateTestRequest, UpdateTestRequest
from module_core.domain.test.router.response.schema import DetailTestResponse, ListDetailTestResponse

# *
# 특정 도메인 서비스의 비즈니스 로직 규격을 정의하는 추상 클래스(인터페이스)입니다.
# 이 클래스를 상속받는 구현체(Service)는 반드시 아래 정의된 인터페이스를 모두 구현해야 합니다.
# *
class AbstractTestService(ABC):
    @abstractmethod
    async def create_test(self, request: CreateTestRequest):
        pass

    @abstractmethod
    async def get_test(self, id: int) -> DetailTestResponse:
        pass

    @abstractmethod
    async def get_test_list(self) -> ListDetailTestResponse:
        pass

    @abstractmethod
    async def update_test(self, id: int, request: UpdateTestRequest) -> DetailTestResponse:
        pass

    @abstractmethod
    async def delete_test(self, id: int) -> None:
        pass