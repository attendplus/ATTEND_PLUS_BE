from fastapi import APIRouter

from module_core.domain.test.router.router import router as test_router
from module_core.router import router as health_check_router

# *
# 각 도메인별로 분리된 하위 라우터들을 하나의 진입점으로 통합합니다.
# 모든 API 경로는 '/api/v1' 프리픽스(Prefix)가 공통으로 적용됩니다.
# *
router = APIRouter(prefix="/api/v1")

# 도메인 및 기능별 라우터 등록
router.include_router(test_router)
router.include_router(health_check_router)
