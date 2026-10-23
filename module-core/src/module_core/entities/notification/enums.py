from enum import Enum

class NotificationType(Enum):
    LATE = "지각"
    QR = "QR"
    SUMMARY = "출석현황"
