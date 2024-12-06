from pydantic.v1 import BaseModel as _BaseModel
from pydantic.v1 import Extra


class BaseModel(_BaseModel):
    class Config:
        extra = Extra.ignore
        arbitrary_types_allowed = True
