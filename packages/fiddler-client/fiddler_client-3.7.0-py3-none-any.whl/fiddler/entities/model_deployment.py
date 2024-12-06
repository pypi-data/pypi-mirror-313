from __future__ import annotations

from datetime import datetime
import logging
from typing import Any
from uuid import UUID

from fiddler.decorators import handle_api_error
from fiddler.entities.base import BaseEntity
from fiddler.entities.job import Job
from fiddler.entities.project import ProjectCompactMixin
from fiddler.schemas.job import JobCompactResp
from fiddler.schemas.model_deployment import ModelDeploymentResponse

logger = logging.getLogger(__name__)


class ModelDeployment(BaseEntity, ProjectCompactMixin):  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        model_id: UUID | str,
    ) -> None:
        """Construct a model deployment instance."""
        self.id: UUID | None = None  # pylint: disable=invalid-name
        self.model_id = model_id
        self.artifact_type: str | None = None
        self.deployment_type: str | None = None
        self.active: bool | None = None
        self.image_uri: str | None = None
        self.replicas: int | None = None
        self.cpu: int | None = None
        self.memory: int | None = None
        self.created_at: datetime | None = None
        self.updated_at: datetime | None = None

        # Deserialized response object
        self._resp: ModelDeploymentResponse | None = None

    @staticmethod
    def _get_url(model_id: UUID | str) -> str:
        """Get model deployment url."""
        return f'v3/models/{model_id}/deployment'

    @classmethod
    def _from_dict(cls, data: dict) -> ModelDeployment:
        """Build entity object from the given dictionary."""

        # Deserialize the response
        resp_obj = ModelDeploymentResponse(**data)
        # Initialize
        instance = cls(
            model_id=resp_obj.model.id,
        )

        # Add remaining fields
        fields = [
            'id',
            'artifact_type',
            'deployment_type',
            'active',
            'image_uri',
            'replicas',
            'cpu',
            'memory',
            'created_at',
            'updated_at',
        ]
        for field in fields:
            setattr(instance, field, getattr(resp_obj, field, None))

        instance._resp = resp_obj
        return instance

    def _refresh(self, data: dict) -> None:
        """Refresh the fields of this instance from the given response dictionary"""
        # Deserialize the response
        resp_obj = ModelDeploymentResponse(**data)

        fields = [
            'id',
            'artifact_type',
            'deployment_type',
            'active',
            'image_uri',
            'replicas',
            'cpu',
            'memory',
            'created_at',
            'updated_at',
        ]
        for field in fields:
            setattr(self, field, getattr(resp_obj, field, None))

        self._resp = resp_obj

    @handle_api_error
    def update(self) -> Job:
        """Update an existing model deployment."""
        payload: dict[str, Any] = {'active': self.active}
        if self.replicas is not None:
            payload['replicas'] = self.replicas
        if self.cpu is not None:
            payload['cpu'] = self.cpu
        if self.memory is not None:
            payload['memory'] = self.memory

        response = self._client().patch(
            url=self._get_url(model_id=self.model_id),
            data=payload,
            headers={'Content-Type': 'application/json'},
        )
        self._refresh_from_response(response=response)
        job_compact = JobCompactResp(**response.json()['data']['job'])
        return Job.get(id_=job_compact.id)

    @classmethod
    def of(cls, model_id: UUID | str) -> ModelDeployment:
        """
        Get model deployment instance of the given model

        :param model_id: Model identifier
        :return: ModelDeployment instance
        """
        response = cls._client().get(url=cls._get_url(model_id=model_id))
        return cls._from_dict(data=response.json()['data'])
