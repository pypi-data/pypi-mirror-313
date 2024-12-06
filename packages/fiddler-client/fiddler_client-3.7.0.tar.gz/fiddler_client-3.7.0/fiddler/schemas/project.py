from datetime import datetime
from uuid import UUID

from fiddler.schemas.base import BaseModel
from fiddler.schemas.organization import OrganizationCompactResp


class ProjectCompactResp(BaseModel):
    id: UUID
    name: str


class ProjectResp(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

    organization: OrganizationCompactResp
