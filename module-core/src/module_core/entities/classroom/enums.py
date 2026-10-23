from enum import Enum

class Status(Enum):
    PENDING = "대기"
    APPROVED = "승인"
    REJECTED = "거절"
    LEFT = "탈퇴"
