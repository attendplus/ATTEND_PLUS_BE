from enum import Enum

class GenderEnum(Enum):
  MALE = "남성"
  FEMALE = "여성"

class RoleEnum(Enum):
  STUDENT = "학생"
  TEACHER = "교사"
  SCHOOL_ADMIN = "학교 관리자"

class EmploymentStatusEnum(Enum):
  EMPLOYEE = "재직"
  RETIRED = "퇴직"
  JOB_CHANGED = "이직"
  ON_LEAVE = "휴직"

class PlatformEnum(Enum):
    IOS = "iOS"
    ANDROID = "Android"
