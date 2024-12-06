from typing import Optional
from uuid import UUID

from fiddler.constants.dataset import EnvType
from fiddler.schemas.base import BaseModel
from fiddler.schemas.model import ModelCompactResp
from fiddler.schemas.organization import OrganizationCompactResp
from fiddler.schemas.project import ProjectCompactResp


class DatasetCompactResp(BaseModel):
    """Dataset Compact."""

    id: UUID
    name: str
    type: EnvType


class DatasetResp(BaseModel):
    """Dataset response pydantic model."""

    id: UUID
    name: str
    row_count: Optional[int]
    model: ModelCompactResp
    project: ProjectCompactResp
    organization: OrganizationCompactResp
