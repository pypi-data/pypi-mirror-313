from datetime import datetime
from uuid import UUID

from fiddler.schemas.base import BaseModel


class OrganizationCompactResp(BaseModel):
    id: UUID
    name: str


class OrganizationResp(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime
