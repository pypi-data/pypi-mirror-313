from datetime import datetime
from typing import List, Optional, Union
from uuid import UUID

from pydantic.v1 import Field

from fiddler.constants.alert_rule import AlertCondition, BinSize, CompareTo, Priority
from fiddler.schemas.base import BaseModel
from fiddler.schemas.baseline import BaselineCompactResp
from fiddler.schemas.custom_expression import SegmentCompactResp
from fiddler.schemas.model import ModelCompactResp
from fiddler.schemas.project import ProjectCompactResp


class MetricResp(BaseModel):
    id: Union[str, UUID]
    display_name: str
    type: str
    type_display_name: str


class AlertRuleResp(BaseModel):
    id: UUID
    name: str
    priority: Union[str, Priority]
    compare_to: Union[str, CompareTo]
    condition: Union[str, AlertCondition]
    compare_bin_delta: Optional[int]
    evaluation_delay: int
    bin_size: Union[str, BinSize]
    columns: Optional[List[str]] = Field(alias='feature_names')
    critical_threshold: float
    warning_threshold: Optional[float]

    created_at: datetime
    updated_at: datetime

    metric: MetricResp
    model: ModelCompactResp
    project: ProjectCompactResp
    baseline: Optional[BaselineCompactResp]
    segment: Optional[SegmentCompactResp]


class NotificationConfig(BaseModel):
    emails: Optional[List[str]]
    pagerduty_services: Optional[List[str]]
    pagerduty_severity: Optional[str]
    webhooks: Optional[List[UUID]]
