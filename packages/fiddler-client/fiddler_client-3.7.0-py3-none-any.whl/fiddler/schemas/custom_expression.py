from datetime import datetime
from typing import Optional
from uuid import UUID

from fiddler.schemas.base import BaseModel
from fiddler.schemas.model import ModelCompactResp
from fiddler.schemas.organization import OrganizationCompactResp
from fiddler.schemas.project import ProjectCompactResp
from fiddler.schemas.user import UserCompactResp


class CustomExpressionResp(BaseModel):
    id: UUID
    name: str
    definition: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    model: ModelCompactResp
    project: ProjectCompactResp
    organization: OrganizationCompactResp
    created_by: UserCompactResp
    updated_by: UserCompactResp


class CustomMetricResp(CustomExpressionResp):
    """Custom metric response object"""


class SegmentResp(CustomExpressionResp):
    """Segment response object"""


class SegmentCompactResp(BaseModel):
    """Segment compact response object"""

    id: UUID
    name: str
