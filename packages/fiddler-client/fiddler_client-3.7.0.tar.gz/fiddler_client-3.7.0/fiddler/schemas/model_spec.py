from typing import List, Union

from pydantic.v1 import BaseModel, Field

from fiddler.schemas.custom_features import (
    Enrichment,
    ImageEmbedding,
    Multivariate,
    TextEmbedding,
    VectorFeature,
)


class ModelSpec(BaseModel):
    """Model spec defines how model columns are used along with model task"""

    schema_version: int = 1
    """Schema version"""

    inputs: List[str] = Field(default_factory=list)
    """Feature columns"""

    outputs: List[str] = Field(default_factory=list)
    """Prediction columns"""

    targets: List[str] = Field(default_factory=list)
    """Label columns"""

    decisions: List[str] = Field(default_factory=list)
    """Decisions columns"""

    metadata: List[str] = Field(default_factory=list)
    """Metadata columns"""

    custom_features: List[
        Union[Multivariate, VectorFeature, TextEmbedding, ImageEmbedding, Enrichment]
    ] = Field(default_factory=list)
    """Custom feature definitions"""

    def remove_column(self, column_name: str) -> None:
        """Remove a column name from spec if it exists."""
        column_lists = [
            self.inputs,
            self.outputs,
            self.targets,
            self.decisions,
            self.metadata,
        ]

        for cols in column_lists:
            if column_name in cols:  # pylint: disable=unsupported-membership-test
                cols.remove(column_name)  # pylint: disable=no-member
                break
