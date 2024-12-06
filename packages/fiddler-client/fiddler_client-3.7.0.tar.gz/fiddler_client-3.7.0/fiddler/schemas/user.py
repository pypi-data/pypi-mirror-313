from uuid import UUID

from pydantic.v1 import BaseModel


class UserCompactResp(BaseModel):
    id: UUID
    full_name: str
    email: str
