# HTTP Status & API Response Payload
from enum import Enum
from http import HTTPStatus
from pydantic import BaseModel

class APIResponseFormat(BaseModel):
    http_status: int
    code: str
    message: str

class ErrorStatus(Enum):
    # 공통 에러
    INTERNAL_SERVER_ERROR = (HTTPStatus.INTERNAL_SERVER_ERROR, "COMMON500", "서버 에러, 관리자에게 문의 바랍니다.")
    BAD_REQUEST = (HTTPStatus.BAD_REQUEST, "COMMON400", "잘못된 요청입니다.")
    UNAUTHORIZED = (HTTPStatus.UNAUTHORIZED, "COMMON401", "인증이 필요합니다.")
    FORBIDDEN = (HTTPStatus.FORBIDDEN, "COMMON403", "금지된 요청입니다.")
    INVALID_PARAMETER = (HTTPStatus.BAD_REQUEST, "COMMON404", "유효하지 않은 파라미터입니다.")

    # 인증 관련 에러
    JWT_ROLE_ERROR = (HTTPStatus.FORBIDDEN, "AUTH400", "현재 권한으로는 실행할 수 없는 기능입니다.")
    JWT_AUTH_ERROR = (HTTPStatus.UNAUTHORIZED, "AUTH401", "로그인 후 다시 접근해주시기 바랍니다.")
    INVALID_TOKEN = (HTTPStatus.UNAUTHORIZED, "AUTH402", "유효하지 않은 토큰입니다.")

    # FILE 관련 에러
    FILE_CONVERT_FAIL = (HTTPStatus.INTERNAL_SERVER_ERROR, "FILE500", "파일 변환 중 에러가 발생했습니다.")
    FILE_NOT_UPLOADED = (HTTPStatus.BAD_REQUEST, "FILE502", "파일이 업로드되지 않았습니다.")
    FILE_NOT_IMAGE = (HTTPStatus.BAD_REQUEST, "FILE400", "이미지 파일이 아닙니다.")
    FILE_DELETE_FAIL = (HTTPStatus.INTERNAL_SERVER_ERROR, "FILE503", "파일 삭제 중 에러가 발생했습니다.")

    def __init__(self, http_status: HTTPStatus, code: str, message: str):
        self._http_status = http_status
        self._code = code
        self._message = message

    def get_message(self, custom_message: str | None = None) -> str:
        return custom_message if custom_message else self._message

    def get_reason_http_status(self) -> APIResponseFormat:
        return APIResponseFormat(
            http_status=self._http_status.value,
            code=self._code,
            message=self._message
        )

class SuccessStatus(Enum):
    OK = (HTTPStatus.OK, "COMMON200", "요청이 승인되었습니다.")

    def __init__(self, http_status: HTTPStatus, code: str, message: str):
        self._http_status = http_status
        self._code = code
        self._message = message

    def get_message(self, custom_message: str | None = None) -> str:
        return custom_message if custom_message else self._message
    