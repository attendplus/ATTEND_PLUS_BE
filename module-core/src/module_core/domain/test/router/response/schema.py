from datetime import datetime
from pydantic import BaseModel

class UploadImageResponse(BaseModel):
    filename: str

class DetailTestResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

class ListDetailTestResponse(BaseModel):
    tests: list[DetailTestResponse]
