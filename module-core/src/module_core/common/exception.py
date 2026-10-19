# Global Exception
from typing import Optional

from module_core.common.type import ErrorStatus, APIResponseFormat

class GlobalException(Exception):
    def __init__(self, code: ErrorStatus, message: Optional[str] = None):
        _message = code.get_message(message)
        super().__init__(_message)
        self.code = code

    def get_error_reason_http_status(self) -> APIResponseFormat:
        return self.code.get_reason_http_status()
