from typing import List, Optional

from fiddler.schemas.base import BaseModel


class ModelTaskParams(BaseModel):
    binary_classification_threshold: Optional[float] = None
    """Threshold for labels"""

    target_class_order: Optional[List] = None
    """Order of target classes"""

    group_by: Optional[str] = None
    """Query/session id column for ranking models"""

    top_k: Optional[int] = None
    """Top k results to consider when computing ranking metrics"""

    class_weights: Optional[List[float]] = None
    """Weight of each classes"""

    weighted_ref_histograms: Optional[bool] = None
    """Whether baseline histograms must be weighted or not while drift metrics"""
