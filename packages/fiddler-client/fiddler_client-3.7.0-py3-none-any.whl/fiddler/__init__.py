from __future__ import annotations

from fiddler.connection import Connection, ConnectionMixin, init  # noqa
from fiddler.constants.alert_rule import (  # noqa
    AlertCondition,
    BinSize,
    CompareTo,
    Priority,
)
from fiddler.constants.baseline import BaselineType, WindowBinSize  # noqa
from fiddler.constants.dataset import EnvType  # noqa
from fiddler.constants.job import JobStatus  # noqa
from fiddler.constants.model import (  # noqa
    ArtifactStatus,
    CustomFeatureType,
    DataType,
    ModelInputType,
    ModelTask,
)
from fiddler.constants.model_deployment import ArtifactType, DeploymentType  # noqa
from fiddler.constants.xai import DownloadFormat, ExplainMethod  # noqa
from fiddler.entities.alert_record import AlertRecord  # noqa
from fiddler.entities.alert_rule import AlertRule  # noqa
from fiddler.entities.baseline import Baseline, BaselineCompact  # noqa
from fiddler.entities.custom_expression import CustomMetric, Segment  # noqa
from fiddler.entities.dataset import Dataset, DatasetCompact  # noqa
from fiddler.entities.file import File  # noqa
from fiddler.entities.job import Job  # noqa
from fiddler.entities.model import Model, ModelCompact  # noqa
from fiddler.entities.model_deployment import ModelDeployment  # noqa
from fiddler.entities.project import Project, ProjectCompact  # noqa
from fiddler.entities.webhook import Webhook  # noqa
from fiddler.exceptions import (  # noqa
    ApiError,
    AsyncJobFailed,
    Conflict,
    ConnError,
    ConnTimeout,
    HttpError,
    IncompatibleClient,
    NotFound,
    Unsupported,
)
from fiddler.schemas.custom_features import (  # noqa
    CustomFeature,
    Enrichment,
    ImageEmbedding,
    Multivariate,
    TextEmbedding,
    VectorFeature,
)
from fiddler.schemas.model_deployment import DeploymentParams  # noqa
from fiddler.schemas.model_schema import Column, ModelSchema  # noqa
from fiddler.schemas.model_spec import ModelSpec  # noqa
from fiddler.schemas.model_task_params import ModelTaskParams  # noqa
from fiddler.schemas.xai import (  # noqa
    DatasetDataSource,
    EventIdDataSource,
    RowDataSource,
)
from fiddler.schemas.xai_params import XaiParams  # noqa
from fiddler.utils.helpers import group_by  # noqa
from fiddler.utils.logger import set_logging  # noqa
from fiddler.version import __version__  # noqa

# Global connection object
conn: Connection | None = None


def _set_conn(conn_: Connection) -> None:
    """Set global conn variable"""
    global conn
    conn = conn_


__all__ = [
    '__version__',
    'Connection',
    'ConnectionMixin',
    'init',
    'conn',
    # Constants
    'AlertCondition',
    'ArtifactStatus',
    'ArtifactType',
    'BaselineType',
    'BinSize',
    'CompareTo',
    'DataType',
    'DeploymentType',
    'DownloadFormat',
    'EnvType',
    'ExplainMethod',
    'JobStatus',
    'ModelInputType',
    'ModelTask',
    'Priority',
    'WindowBinSize',
    # Schemas
    'CustomFeature',
    'DatasetDataSource',
    'DeploymentParams',
    'Enrichment',
    'EventIdDataSource',
    'ImageEmbedding',
    'ModelSchema',
    'Column',
    'ModelSpec',
    'ModelTaskParams',
    'Multivariate',
    'RowDataSource',
    'TextEmbedding',
    'VectorFeature',
    'XaiParams',
    # Entities
    'AlertRecord',
    'AlertRule',
    'Baseline',
    'BaselineCompact',
    'Dataset',
    'DatasetCompact',
    'CustomMetric',
    'File',
    'Job',
    'Model',
    'ModelCompact',
    'ModelDeployment',
    'Project',
    'ProjectCompact',
    'Segment',
    'Webhook',
    # Exceptions
    'NotFound',
    'Conflict',
    'IncompatibleClient',
    'AsyncJobFailed',
    'Unsupported',
    'HttpError',
    'ConnTimeout',
    'ConnError',
    'ApiError',
    # Utilities
    'set_logging',
    'group_by',
]
