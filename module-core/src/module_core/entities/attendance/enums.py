from enum import Enum

class Status(Enum):
    PRESENT = "출석인정"
    ABSENT = "결석"
    LATE = "지각"
    EARLY_LEAVE = "조퇴"
    PENDING = "보류"

class Method(Enum):
    GPS = "QPS"
    QR = "QR"
    MANUAL = "수동"

class ReasonType(Enum):
    ILLNESS = "질병"
    UNEXCUSED = "무단"
    OTHER = "기타"
