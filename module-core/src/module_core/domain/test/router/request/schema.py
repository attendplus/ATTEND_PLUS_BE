from pydantic import BaseModel, Field

# *
# frozen=True 옵션을 적용하여, 요청 객체(Request Object)를 안전한 불변(Immutable) 상태로 관리합니다.
# *
class CreateTestRequest(BaseModel):
    model_config = { "frozen": True }

    title: str = Field(min_length=2, max_length=20)
    content: str

class UpdateTestRequest(BaseModel):
    model_config = { "frozen": True }

    title: str = Field(min_length=2, max_length=20)
    content: str
    