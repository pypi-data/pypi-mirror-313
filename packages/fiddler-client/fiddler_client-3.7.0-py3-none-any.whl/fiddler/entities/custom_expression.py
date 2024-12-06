from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from typing import Any, Iterator
from uuid import UUID

from fiddler.decorators import handle_api_error
from fiddler.entities.base import BaseEntity
from fiddler.entities.model import ModelCompactMixin
from fiddler.entities.project import ProjectCompactMixin
from fiddler.schemas.custom_expression import (
    CustomExpressionResp,
    CustomMetricResp,
    SegmentResp,
)
from fiddler.schemas.filter_query import OperatorType, QueryCondition, QueryRule
from fiddler.utils.helpers import raise_not_found


class CustomExpression(BaseEntity, ModelCompactMixin, ProjectCompactMixin):
    def __init__(
        self,
        name: str,
        model_id: UUID | str,
        definition: str,
        description: str | None = None,
    ) -> None:
        """Construct a custom expression instance."""
        self.name = name
        self.model_id = model_id
        self.definition = definition
        self.description = description

        self.id: UUID | None = None
        self.created_at: datetime | None = None

        # Deserialized response object
        self._resp: CustomExpressionResp | None = None

    @classmethod
    def _get_url(cls, id_: UUID | str | None = None) -> str:
        """Get custom expression resource/item url."""
        url = f'/v3/{cls._get_url_path()}'
        return url if not id_ else f'{url}/{id_}'

    @staticmethod
    @abstractmethod
    def _get_url_path() -> str:
        """Get custom expression resource path"""

    @staticmethod
    @abstractmethod
    def _get_display_name() -> str:
        """Get custom expression display name"""

    def _refresh(self, data: dict) -> None:
        """Refresh the fields of this instance from the given response dictionary"""
        # Deserialize the response
        resp_obj = CustomMetricResp(**data)
        assert self.model_id
        fields = [
            'id',
            'name',
            'definition',
            'description',
            'created_at',
        ]
        for field in fields:
            setattr(self, field, getattr(resp_obj, field, None))

        self._resp = resp_obj

    @classmethod
    def _from_dict(cls, data: dict) -> CustomExpression:
        """Build entity object from the given dictionary."""

        # Deserialize the response
        resp_obj = CustomMetricResp(**data)

        # Initialize
        instance = cls(
            name=resp_obj.name,
            model_id=resp_obj.model.id,
            definition=resp_obj.definition,
            description=resp_obj.description,
        )

        # Add remaining fields
        fields = [
            'id',
            'created_at',
        ]
        for field in fields:
            setattr(instance, field, getattr(resp_obj, field, None))

        instance._resp = resp_obj

        return instance

    @classmethod
    @handle_api_error
    def get(cls, id_: UUID | str) -> CustomExpression:
        """
        Get the CustomMetric instance using custom metric id.

        :param id_: unique uuid format identifier for custom metric
        :return: CustomMetric instance
        """
        response = cls._client().get(url=cls._get_url(id_=id_))
        return cls._from_response(response=response)

    @classmethod
    @handle_api_error
    def from_name(cls, name: str, model_id: UUID | str) -> CustomExpression:
        """
        Get the custom metric instance of a model from custom metric name

        :param name: Custom metric name
        :param model_id: Model identifier

        :return: CustomMetric instance for the provided params
        """

        _filter = QueryCondition(
            rules=[
                QueryRule(field='name', operator=OperatorType.EQUAL, value=name),
                QueryRule(
                    field='model_id', operator=OperatorType.EQUAL, value=model_id
                ),
            ]
        )
        params: dict[str, Any] = {
            'filter': _filter.json(),
        }

        response = cls._client().get(
            url=cls._get_url(),
            params=params,
        )
        if response.json()['data']['total'] == 0:
            raise_not_found(
                f'{cls._get_display_name()} not found for the given identifier'
            )

        return cls._from_dict(data=response.json()['data']['items'][0])

    @classmethod
    @handle_api_error
    def list(
        cls,
        model_id: UUID | str,
    ) -> Iterator[CustomExpression]:
        """Get a list of all custom metrics in the organization."""

        url = f'/v3/models/{model_id}/{cls._get_url_path()}'

        for item in cls._paginate(url=url):
            yield cls._from_dict(data=item)

    @handle_api_error
    def create(self) -> CustomExpression:
        """Create a new custom metric."""
        payload = {
            'model_id': self.model_id,
            'name': self.name,
            'definition': self.definition,
        }

        if self.description:
            payload['description'] = self.description

        response = self._client().post(
            url=self._get_url(),
            data=payload,
            headers={'Content-Type': 'application/json'},
        )
        self._refresh_from_response(response=response)
        return self

    @handle_api_error
    def delete(self) -> None:
        """Delete a custom metric."""
        assert self.id is not None

        self._client().delete(url=self._get_url(id_=self.id))


class CustomMetric(CustomExpression):
    def __init__(
        self,
        name: str,
        model_id: UUID | str,
        definition: str,
        description: str | None = None,
    ) -> None:
        """Construct a custom metric instance."""
        super().__init__(name, model_id, definition, description)

        # Deserialized response object
        self._resp: CustomMetricResp | None = None

    @staticmethod
    def _get_url_path() -> str:
        return 'custom-metrics'

    @staticmethod
    def _get_display_name() -> str:
        return 'Custom metric'


class Segment(CustomExpression):
    def __init__(
        self,
        name: str,
        model_id: UUID | str,
        definition: str,
        description: str | None = None,
    ) -> None:
        """Construct a segment instance."""
        super().__init__(name, model_id, definition, description)

        # Deserialized response object
        self._resp: SegmentResp | None = None

    @staticmethod
    def _get_url_path() -> str:
        return 'segments'

    @staticmethod
    def _get_display_name() -> str:
        return 'Segment'
