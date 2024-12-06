import enum
from datetime import datetime
from uuid import UUID

from pydantic.fields import Field

from fiddler.schemas.base import BaseModel


@enum.unique
class WebhookProvider(str, enum.Enum):
    # provider is 'SLACK' or 'OTHER' as of Aug 2023.
    SLACK = 'SLACK'
    OTHER = 'OTHER'


class WebhookResp(BaseModel):
    id: UUID = Field(alias='uuid')
    name: str
    url: str
    provider: WebhookProvider
    created_at: datetime
    updated_at: datetime
