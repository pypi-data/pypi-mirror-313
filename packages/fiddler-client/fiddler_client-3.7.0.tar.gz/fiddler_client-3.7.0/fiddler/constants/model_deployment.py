from __future__ import annotations

import enum


@enum.unique
class DeploymentType(str, enum.Enum):
    BASE_CONTAINER = 'BASE_CONTAINER'
    MANUAL = 'MANUAL'


@enum.unique
class ArtifactType(str, enum.Enum):
    SURROGATE = 'SURROGATE'
    PYTHON_PACKAGE = 'PYTHON_PACKAGE'
