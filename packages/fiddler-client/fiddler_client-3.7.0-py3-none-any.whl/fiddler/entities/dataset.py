from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator
from uuid import UUID

from fiddler.constants.dataset import EnvType
from fiddler.decorators import handle_api_error
from fiddler.entities.base import BaseEntity
from fiddler.entities.project import ProjectCompactMixin
from fiddler.schemas.dataset import DatasetResp
from fiddler.schemas.filter_query import OperatorType, QueryCondition, QueryRule
from fiddler.utils.helpers import raise_not_found


class Dataset(BaseEntity, ProjectCompactMixin):
    def __init__(self, name: str, model_id: str | UUID, project_id: UUID | str) -> None:
        """Construct a dataset instance."""
        self.model_id = model_id
        self.project_id = project_id
        self.name = name
        self.row_count: int | None = None

        self.id: UUID | None = None  # pylint: disable=invalid-name

        # Deserialized response object
        self._resp: DatasetResp | None = None

    @staticmethod
    def _get_url(id_: UUID | str | None = None) -> str:
        """Get model resource/item url."""
        url = '/v3/environments'
        return url if not id_ else f'{url}/{id_}'

    @classmethod
    def _from_dict(cls, data: dict) -> Dataset:
        """Build entity object from the given dictionary."""

        # Deserialize the response
        resp_obj = DatasetResp(**data)

        # Initialize
        instance = cls(
            name=resp_obj.name,
            model_id=resp_obj.model.id,
            project_id=resp_obj.project.id,
        )

        # Add remaining fields
        fields = [
            'id',
            'row_count',
        ]
        for field in fields:
            setattr(instance, field, getattr(resp_obj, field, None))

        instance._resp = resp_obj

        return instance

    @classmethod
    @handle_api_error
    def get(cls, id_: UUID | str) -> Dataset:
        """
        Get the dataset instance using dataset id.

        :param id_: unique uuid format identifier for dataset
        :return: dataset instance
        """
        response = cls._client().get(url=cls._get_url(id_=id_))
        return cls._from_response(response=response)

    @classmethod
    @handle_api_error
    def from_name(cls, name: str, model_id: UUID | str) -> Dataset:
        """
        Get the dataset instance using dataset name.

        :param name: Dataset name
        :param model_id: Model identifier

        :return: Dataset instance for the provided params
        """
        _filter = QueryCondition(
            rules=[
                QueryRule(field='name', operator=OperatorType.EQUAL, value=name),
                QueryRule(
                    field='model_id',
                    operator=OperatorType.EQUAL,
                    value=model_id,
                ),
            ]
        )

        response = cls._client().get(
            url=cls._get_url(),
            params={'filter': _filter.json()},
        )

        if response.json()['data']['total'] == 0:
            raise_not_found('Dataset not found for the given identifier')

        return cls._from_dict(data=response.json()['data']['items'][0])

    @classmethod
    @handle_api_error
    def list(cls, model_id: UUID | str) -> Iterator[Dataset]:
        """
        Get a list of all datasets of a model.

        :param model_id: unique uuid format identifier for model
        :return: Iterator of datasets
        """
        params: dict[str, Any] = {'type': EnvType.PRE_PRODUCTION.value}
        url = f'/v3/models/{model_id}/environments'
        for dataset in cls._paginate(url=url, params=params):
            yield cls._from_dict(data=dataset)


@dataclass
class DatasetCompact:
    id: UUID
    name: str

    def fetch(self) -> Dataset:
        """Fetch dataset instance"""
        return Dataset.get(id_=self.id)


class DatasetCompactMixin:
    @property
    def dataset(self) -> DatasetCompact | None:
        """Dataset instance"""
        response = getattr(self, '_resp', None)
        if not response or not hasattr(response, 'dataset'):
            raise AttributeError(
                'This property is available only for objects generated from API '
                'response.'
            )

        if response.dataset.type == EnvType.PRODUCTION:
            return None

        return DatasetCompact(id=response.dataset.id, name=response.dataset.name)
