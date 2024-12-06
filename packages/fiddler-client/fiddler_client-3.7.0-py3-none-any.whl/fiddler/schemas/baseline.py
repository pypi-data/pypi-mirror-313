from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic.v1 import Field

from fiddler.schemas.base import BaseModel
from fiddler.schemas.dataset import DatasetCompactResp
from fiddler.schemas.model import ModelCompactResp
from fiddler.schemas.organization import OrganizationCompactResp
from fiddler.schemas.project import ProjectCompactResp


class BaselineCompactResp(BaseModel):
    id: UUID
    name: str


class BaselineResp(BaseModel):
    """Baseline response pydantic model."""

    id: UUID
    name: str
    type: str
    start_time: Optional[int]
    end_time: Optional[int]
    offset_delta: Optional[int]
    window_bin_size: Optional[str]
    row_count: Optional[int]

    model: ModelCompactResp
    project: ProjectCompactResp
    organization: OrganizationCompactResp
    dataset: DatasetCompactResp = Field(alias='environment')

    created_at: datetime
    updated_at: datetime
