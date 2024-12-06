from unittest import mock

import pytest

from fiddler.constants.dataset import EnvType
from fiddler.entities.baseline import BaselineCompact, BaselineCompactMixin
from fiddler.entities.dataset import DatasetCompact, DatasetCompactMixin
from fiddler.entities.model import ModelCompact, ModelCompactMixin
from fiddler.entities.project import ProjectCompact, ProjectCompactMixin
from fiddler.entities.user import CreatedByMixin, UpdatedByMixin, UserCompact
from fiddler.schemas.baseline import BaselineCompactResp
from fiddler.schemas.dataset import DatasetCompactResp
from fiddler.schemas.model import ModelCompactResp
from fiddler.schemas.project import ProjectCompactResp
from fiddler.schemas.user import UserCompactResp
from fiddler.tests.constants import (
    BASELINE_ID,
    BASELINE_NAME,
    DATASET_ID,
    DATASET_NAME,
    MODEL_ID,
    MODEL_NAME,
    MODEL_VERSION,
    PROJECT_ID,
    PROJECT_NAME,
    USER_EMAIL,
    USER_ID,
    USER_NAME,
)


class DummyEntity(
    ModelCompactMixin,
    ProjectCompactMixin,
    DatasetCompactMixin,
    BaselineCompactMixin,
    CreatedByMixin,
    UpdatedByMixin,
):
    def __init__(self) -> None:
        self._resp = mock.MagicMock()
        self._resp.project = ProjectCompactResp(id=PROJECT_ID, name=PROJECT_NAME)
        self._resp.model = ModelCompactResp(
            id=MODEL_ID, name=MODEL_NAME, version=MODEL_VERSION
        )
        self._resp.dataset = DatasetCompactResp(
            id=DATASET_ID, name=DATASET_NAME, type=EnvType.PRE_PRODUCTION
        )
        self._resp.baseline = BaselineCompactResp(id=BASELINE_ID, name=BASELINE_NAME)
        self._resp.created_by = UserCompactResp(
            id=USER_ID, full_name=USER_NAME, email=USER_EMAIL
        )
        self._resp.updated_by = UserCompactResp(
            id=USER_ID, full_name=USER_NAME, email=USER_EMAIL
        )


@pytest.fixture()
def entity() -> DummyEntity:
    dummy_entity = DummyEntity()
    yield dummy_entity


@pytest.mark.parametrize(
    ('property_name', 'class_name'),
    [
        ('project', ProjectCompact),
        ('dataset', DatasetCompact),
        ('model', ModelCompact),
        ('baseline', BaselineCompact),
        ('created_by', UserCompact),
        ('updated_by', UserCompact),
    ],
)
def test_mixins(entity: DummyEntity, property_name: str, class_name: type) -> None:
    assert isinstance(getattr(entity, property_name), class_name)

    entity._resp = None
    with pytest.raises(AttributeError):
        _ = getattr(entity, property_name)
