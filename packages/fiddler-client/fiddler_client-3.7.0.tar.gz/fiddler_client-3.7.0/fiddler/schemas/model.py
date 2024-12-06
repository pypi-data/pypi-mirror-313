from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic.v1 import Field

from fiddler.schemas.base import BaseModel
from fiddler.schemas.model_schema import ModelSchema
from fiddler.schemas.model_spec import ModelSpec
from fiddler.schemas.model_task_params import ModelTaskParams
from fiddler.schemas.organization import OrganizationCompactResp
from fiddler.schemas.project import ProjectCompactResp
from fiddler.schemas.user import UserCompactResp
from fiddler.schemas.xai_params import XaiParams


class ModelCompactResp(BaseModel):
    id: UUID
    name: str
    version: Optional[str]


class ModelResp(BaseModel):
    id: UUID
    name: str
    version: str
    input_type: str
    task: str
    task_params: ModelTaskParams
    schema_: ModelSchema = Field(alias='schema')
    spec: ModelSpec
    description: Optional[str]
    event_id_col: Optional[str]
    event_ts_col: Optional[str]
    event_ts_format: Optional[str]
    xai_params: Optional[XaiParams]
    artifact_status: str
    artifact_files: List[Dict]
    created_at: datetime
    updated_at: datetime
    created_by: UserCompactResp
    updated_by: UserCompactResp
    organization: OrganizationCompactResp
    project: ProjectCompactResp
    is_binary_ranking_model: bool


class GenerateModelResp(BaseModel):
    schema_: ModelSchema = Field(alias='schema')
    spec: ModelSpec
