import uuid
import traceback

from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from module_core.common.response import ApiResponse
from module_core.common.exception import GlobalException
from module_core.common.type import ErrorStatus, APIResponseFormat
from module_core.common.config.database import QueryLogContext

from attendplus.router import router

app = FastAPI(
    title="Attend Plus API",
    description="Attend Plus Backend API",
    version="beta"
)
app.include_router(router)

# HTTP 요청 추적 및 로그 관리 미들웨어 설정
@app.middleware("http")
async def trace_log_middleware(request: Request, call_next):
    client_host: str = f"{request.client.host}:{request.client.port}" if request.client else "UNKNOWN_IP"
    ip: str = request.headers.get("x-forwarded-for", client_host).split(",")[0].strip()

    route_path: str = request.url.path
    method: str = request.method
    
    QueryLogContext.set({
        "ctx_id": str(uuid.uuid4())[:32],
        "router": f"{method} {route_path}",
        "ip": ip
    })
    
    response = await call_next(request)

    return response

# GlobalException을 감지하는 전역 핸들러 등록
@app.exception_handler(GlobalException)
async def general_exception_handler(req: Request, exc: GlobalException):
    traceback.print_exc()
    
    error_reason: APIResponseFormat = exc.get_error_reason_http_status()
    response_body: ApiResponse = ApiResponse.on_failure(
        code=error_reason.code,
        message=str(exc),
        data=None
    )
    
    return JSONResponse(
        status_code=error_reason.http_status,
        content=response_body.model_dump(by_alias=True, exclude_none=True)
    )

# Exception을 감지하는 전역 핸들러 등록
@app.exception_handler(Exception)
async def value_error_exception_handler(req: Request, exc: Exception):
    traceback.print_exc()

    response_body: ApiResponse = ApiResponse.on_failure(
        code=ErrorStatus.INTERNAL_SERVER_ERROR._code,
        message=str(exc),
        data=None
    )
    
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content=response_body.model_dump(by_alias=True, exclude_none=True)
    )
