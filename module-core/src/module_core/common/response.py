# Common API Response Format
from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field

from module_core.common.type import SuccessStatus

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    is_success: bool = Field(serialization_alias="isSuccess")
    code: str
    message: str
    result: Optional[T] = None

    @classmethod
    def on_success(cls, result: Optional[T] = None) -> ApiResponse[T]:
        return cls(
            is_success=True,
            code=SuccessStatus.OK._code,
            message=SuccessStatus.OK.get_message(),
            result=result
        )

    @classmethod
    def on_failure(cls, code: str, message: str, data: Optional[Any] = None) -> ApiResponse[Any]:
        return cls(
            is_success=False,
            code=code,
            message=message,
            result=data
        )
