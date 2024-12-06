from typing import Optional
from uuid import UUID

from fiddler.schemas.base import BaseModel


class JobCompactResp(BaseModel):
    id: UUID
    name: str


class JobResp(BaseModel):
    id: UUID
    name: str
    status: str
    progress: float
    info: dict
    error_message: Optional[str]
    error_reason: Optional[str]
    extras: Optional[dict]
