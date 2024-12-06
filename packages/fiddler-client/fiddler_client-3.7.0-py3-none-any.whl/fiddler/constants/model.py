from __future__ import annotations

import enum


@enum.unique
class ModelInputType(str, enum.Enum):
    """Input data type used by the model"""

    TABULAR = 'structured'
    TEXT = 'text'
    MIXED = 'mixed'


@enum.unique
class ModelTask(str, enum.Enum):
    """Task the model is designed to address"""

    BINARY_CLASSIFICATION = 'binary_classification'
    MULTICLASS_CLASSIFICATION = 'multiclass_classification'
    REGRESSION = 'regression'
    RANKING = 'ranking'
    LLM = 'llm'
    NOT_SET = 'not_set'

    def is_classification(self) -> bool:
        return self in {
            ModelTask.BINARY_CLASSIFICATION,
            ModelTask.MULTICLASS_CLASSIFICATION,
        }

    def is_regression(self) -> bool:
        return self == ModelTask.REGRESSION


@enum.unique
class DataType(str, enum.Enum):
    """Data types supported for model columns"""

    FLOAT = 'float'
    INTEGER = 'int'
    BOOLEAN = 'bool'
    STRING = 'str'
    CATEGORY = 'category'
    TIMESTAMP = 'timestamp'
    VECTOR = 'vector'

    def is_numeric(self) -> bool:
        return self in {DataType.INTEGER, DataType.FLOAT}

    def is_bool_or_cat(self) -> bool:
        return self in {DataType.BOOLEAN, DataType.CATEGORY}

    def is_vector(self) -> bool:
        return self == DataType.VECTOR


@enum.unique
class ArtifactStatus(str, enum.Enum):
    """Artifact Status"""

    NO_MODEL = 'no_model'
    SURROGATE = 'surrogate'
    USER_UPLOADED = 'user_uploaded'


@enum.unique
class CustomFeatureType(str, enum.Enum):
    FROM_COLUMNS = 'FROM_COLUMNS'
    FROM_VECTOR = 'FROM_VECTOR'
    FROM_TEXT_EMBEDDING = 'FROM_TEXT_EMBEDDING'
    FROM_IMAGE_EMBEDDING = 'FROM_IMAGE_EMBEDDING'
    ENRICHMENT = 'ENRICHMENT'
