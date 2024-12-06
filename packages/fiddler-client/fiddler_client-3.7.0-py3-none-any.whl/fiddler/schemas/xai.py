from typing import Dict, Optional, Union
from uuid import UUID

from pydantic.v1 import Field

from fiddler.constants.dataset import EnvType
from fiddler.schemas.base import BaseModel


class RowDataSource(BaseModel):
    source_type = 'ROW'
    row: Dict


class EventIdDataSource(BaseModel):
    source_type = 'EVENT_ID'
    event_id: str
    env_id: Optional[Union[str, UUID]] = Field(alias='dataset_id')
    env_type: EnvType


class DatasetDataSource(BaseModel):
    source_type = 'ENVIRONMENT'
    env_type: str
    num_samples: Optional[int]
    env_id: Optional[Union[str, UUID]] = Field(alias='dataset_id')
