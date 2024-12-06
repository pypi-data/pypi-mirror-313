from datetime import datetime
from typing import Optional
from uuid import UUID

from fiddler.constants.model_deployment import ArtifactType, DeploymentType
from fiddler.schemas.base import BaseModel
from fiddler.schemas.model import ModelCompactResp
from fiddler.schemas.organization import OrganizationCompactResp
from fiddler.schemas.project import ProjectCompactResp
from fiddler.schemas.user import UserCompactResp


class ModelDeploymentResponse(BaseModel):
    id: UUID
    model: ModelCompactResp
    project: ProjectCompactResp
    organization: OrganizationCompactResp
    artifact_type: str
    deployment_type: str
    active: bool
    image_uri: Optional[str]
    replicas: Optional[int]
    cpu: Optional[int]
    memory: Optional[int]
    created_at: datetime
    updated_at: datetime
    created_by: UserCompactResp
    updated_by: UserCompactResp


class DeploymentParams(BaseModel):
    artifact_type: str = ArtifactType.PYTHON_PACKAGE
    deployment_type: DeploymentType = DeploymentType.BASE_CONTAINER
    image_uri: Optional[str]
    replicas: Optional[int]
    cpu: Optional[int]
    memory: Optional[int]
