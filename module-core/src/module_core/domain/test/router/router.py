# Router Layer
from module_core.domain.test.service.service import test_service

from fastapi import APIRouter, UploadFile, File

from module_core.domain.test.router.request.schema import CreateTestRequest, UpdateTestRequest
from module_core.domain.test.router.response.schema import UploadImageResponse, DetailTestResponse, ListDetailTestResponse

from module_core.common.response import ApiResponse
from module_core.common.exception import GlobalException
from module_core.common.type import ErrorStatus

# *
# test 패키지는 컨벤션 문서용 패키지입니다.
# 최소한의 컨벤션은 필요한데, 따로 문서화하기엔 시간이 너무 걸릴 것 같아 주석으로 대체합니다.
# 
# 추가로, 해당 컨벤션 내용은 혹시나 개발을 헤매실까봐 전부 참고용으로 적는 것입니다!
# 본인만의 편한 방식이 있다면, 그대로 개발하셔도 당연히 당연히 좋습니다.

# < Router >
# prefix, tags는 router별로 수정해주세요!
# ex) router = APIRouter(prefix="/test", tags=["Test 관련 API"])
# *
router = APIRouter(prefix="/test", tags=["Test 관련 API"])

# *
# Router부터 Repository까지 연결된 메서드는 이름을 통일해 주세요!
# 앞으로 유지보수하기 편할 것 같습니다. 또한 클래스를 제외한 모든 함수는 스네이크 케이스(Snake Case)를 사용합니다.
#
# 요청 DTO, 응답 DTO도 이름 형식을 맞춰주세요.
# 생성 관련 : CreateXXXRequest / CreateXXXResponse
# 상세 조회 관련 : DetailXXXRequest / DetailXXXResponse
# 목록 조회 관련 : ListDetailXXXRequest / ListDetailXXXResponse
# 수정 관련 : UpdateXXXRequest / UpdateXXXResponse
# *

@router.post(path="/create", summary="테스트 생성 엔드포인트", response_model=ApiResponse)
async def create(request: CreateTestRequest) -> ApiResponse:
    await test_service.create_test(request)
    return ApiResponse.on_success()

@router.get(path="/list", summary="테스트 목록 상세 조회 엔드포인트", response_model=ApiResponse)
async def get_test_list() -> ApiResponse:
    list: ListDetailTestResponse = await test_service.get_test_list()
    return ApiResponse.on_success(list)

@router.post("/upload", summary="단일 이미지 업로드 엔드포인트", response_model=ApiResponse)
async def upload_profile_image(file: UploadFile | None = File(None)) -> ApiResponse:
    if not file:
        raise GlobalException(ErrorStatus.FILE_NOT_UPLOADED)
        # raise ValueError("값이 옳바르지 않습니다.")
        
    if not file.content_type or not file.content_type.startswith("image/"):
        raise GlobalException(
            code=ErrorStatus.FILE_NOT_IMAGE, 
            message=f"업로드하신 {file.filename or '파일'}은 올바른 이미지 포맷이 아닙니다."
        )

    return ApiResponse.on_success(
        UploadImageResponse(filename=file.filename or "unknown_file")
    )

# *
# FastAPI는 라우터에 등록된 순서대로(Top-down) 경로 매칭을 시도합니다. 이로 인한 오동작을 방지하기 위해 아래 규칙을 반드시 준수해 주세요!
# 경로 파라미터(Path Parameter)가 포함된 엔드포인트는 반드시 파라미터가 없는 고정 경로(Static Path) 엔드포인트 뒤에 작성해야 합니다.
# 순서의 차이가 있으니 주의해 주세요!
# *
@router.patch("/update/{id}", summary="특정 테스트 수정 엔드포인트", response_model=ApiResponse)
async def update_test(id: int, request: UpdateTestRequest) -> ApiResponse:
    result: DetailTestResponse = await test_service.update_test(id, request)
    return ApiResponse.on_success(result)

@router.get("/{id}", summary="특정 테스트 조회 엔드포인트", response_model=ApiResponse)
async def get_test(id: int) -> ApiResponse:
    result: DetailTestResponse = await test_service.get_test(id)
    return ApiResponse.on_success(result)

@router.delete("/{id}", summary="특정 테스트 삭제 엔드포인트", response_model=ApiResponse)
async def delete_test(id: int) -> ApiResponse:
    await test_service.delete_test(id)
    return ApiResponse.on_success()
