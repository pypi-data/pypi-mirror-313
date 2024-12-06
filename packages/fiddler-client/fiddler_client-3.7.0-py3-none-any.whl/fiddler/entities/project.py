from __future__ import annotations

import logging
import typing
from dataclasses import dataclass
from datetime import datetime
from typing import Iterator
from uuid import UUID

from fiddler.decorators import handle_api_error
from fiddler.entities.base import BaseEntity
from fiddler.exceptions import NotFound
from fiddler.schemas.filter_query import OperatorType, QueryCondition, QueryRule
from fiddler.schemas.project import ProjectResp
from fiddler.utils.helpers import raise_not_found

logger = logging.getLogger(__name__)

if typing.TYPE_CHECKING:
    from fiddler.entities.model import ModelCompact


class Project(BaseEntity):
    def __init__(self, name: str) -> None:
        """
        Construct a project instance

        :param name: Slug like name
        """
        self.name = name

        self.id: UUID | None = None
        self.created_at: datetime | None = None
        self.updated_at: datetime | None = None

        # Deserialized response object
        self._resp: ProjectResp | None = None

    @staticmethod
    def _get_url(id_: UUID | str | None = None) -> str:
        """Get project resource/item url"""
        url = '/v3/projects'
        return url if not id_ else f'{url}/{id_}'

    @classmethod
    def _from_dict(cls, data: dict) -> Project:
        """Build entity object from the given dictionary"""

        # Deserialize the response
        resp_obj = ProjectResp(**data)

        # Initialize
        instance = cls(
            name=resp_obj.name,
        )

        # Add remaining fields
        fields = ['id', 'created_at', 'updated_at']
        for field in fields:
            setattr(instance, field, getattr(resp_obj, field, None))

        instance._resp = resp_obj
        return instance

    def _refresh(self, data: dict) -> None:
        """Refresh the fields of this instance from the given response dictionary"""
        # Deserialize the response
        resp_obj = ProjectResp(**data)

        fields = [
            'id',
            'name',
            'created_at',
            'updated_at',
        ]
        for field in fields:
            setattr(self, field, getattr(resp_obj, field, None))

        self._resp = resp_obj

    @classmethod
    @handle_api_error
    def get(cls, id_: UUID | str) -> Project:
        """Get the project instance using project id"""
        response = cls._client().get(url=cls._get_url(id_))
        return cls._from_response(response=response)

    @classmethod
    @handle_api_error
    def from_name(cls, name: str) -> Project:
        """Get the project instance using project name"""
        _filter = QueryCondition(
            rules=[QueryRule(field='name', operator=OperatorType.EQUAL, value=name)]
        )

        response = cls._client().get(
            url=cls._get_url(), params={'filter': _filter.json()}
        )
        if response.json()['data']['total'] == 0:
            raise_not_found('Project not found for the given identifier')

        return cls._from_dict(data=response.json()['data']['items'][0])

    @classmethod
    @handle_api_error
    def list(cls) -> Iterator[Project]:
        """Get a list of all projects in the organization"""
        for project in cls._paginate(url=cls._get_url()):
            yield cls._from_dict(data=project)

    @handle_api_error
    def create(self) -> Project:
        """Create a new project"""
        response = self._client().post(
            url=self._get_url(),
            # Simple object, stdlib JSON encoding good enough.
            json={'name': self.name},
        )
        self._refresh_from_response(response=response)
        return self

    @classmethod
    @handle_api_error
    def get_or_create(cls, name: str) -> Project:
        """Get project instance based on name or create a new one"""
        try:
            return cls.from_name(name=name)
        except NotFound:
            logger.info('Project not found, creating a new one - `%s`', name)
            return Project(name=name).create()

    @handle_api_error
    def delete(self) -> None:
        """Delete project"""
        # @TODO - Switch this to v3 once we have the endpoint
        self._client().delete(url=f'/v2/projects/{self.organization_name}:{self.name}')

    @property
    def models(self) -> Iterator[ModelCompact]:
        """Fetch all the models of this project"""
        from fiddler.entities.model import (  # pylint: disable=import-outside-toplevel
            Model,
        )

        assert self.id is not None

        yield from Model.list(project_id=self.id)


@dataclass
class ProjectCompact:
    id: UUID
    name: str

    def fetch(self) -> Project:
        """Fetch project instance"""
        return Project.get(id_=self.id)


class ProjectCompactMixin:
    @property
    def project(self) -> ProjectCompact:
        """Project instance"""
        response = getattr(self, '_resp', None)
        if not response or not hasattr(response, 'project'):
            raise AttributeError(
                'This property is available only for objects generated from API '
                'response.'
            )

        return ProjectCompact(id=response.project.id, name=response.project.name)
