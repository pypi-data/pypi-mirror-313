from typing import List, Optional

from pydantic.v1 import BaseModel


class XaiParams(BaseModel):
    custom_explain_methods: List[str] = []
    """User-defined explain_custom method of the model object defined in package.py"""

    default_explain_method: Optional[str] = None
    """Default explanation method"""
