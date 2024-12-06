from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic.v1 import Field

from fiddler.schemas.base import BaseModel


class AlertRecordResp(BaseModel):
    id: UUID = Field(alias='uuid')
    alert_rule_id: UUID = Field(alias='alert_config_uuid')
    alert_run_start_time: int
    alert_time_bucket: int
    alert_value: float
    baseline_time_bucket: Optional[int]
    baseline_value: Optional[float]
    is_alert: bool
    severity: str
    failure_reason: str
    message: str
    feature_name: Optional[str]
    alert_record_main_version: int
    alert_record_sub_version: int

    created_at: datetime
    updated_at: datetime
