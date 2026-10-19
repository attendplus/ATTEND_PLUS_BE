from typing import Dict
from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health Check 관련 API"]
)

@router.get("", summary="헬스체크 엔드포인트", response_model=Dict[str, str])
async def health() -> Dict[str, str]:
    return { "status": "OK" }
