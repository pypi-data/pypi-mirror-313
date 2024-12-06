from __future__ import annotations

import logging
from typing import Any
from uuid import UUID

from fiddler.connection import ConnectionMixin
from fiddler.constants.model_deployment import ArtifactType
from fiddler.decorators import handle_api_error
from fiddler.entities.job import Job
from fiddler.schemas.job import JobCompactResp
from fiddler.schemas.model_deployment import DeploymentParams


logger = logging.getLogger(__name__)


class Surrogate(ConnectionMixin):
    def __init__(self, model_id: UUID) -> None:
        """
        Surrogate model methods

        :param model_id: Model identifier
        """
        self.model_id = model_id

    def _deploy(
        self,
        dataset_id: UUID | str,
        deployment_params: DeploymentParams | None = None,
        update: bool = False,
    ) -> Job:
        """
        Deploy surrogate model to an existing model

        :param dataset_id: Dataset to be used for generating surrogate model
        :param deployment_params: Model deployment parameters
        :param update: Set True for re-generating surrogate model, otherwise False
        :return: Async job
        """

        payload: dict[str, Any] = {
            'env_id': dataset_id,
            'deployment_params': {},
        }

        if deployment_params:
            deployment_params.artifact_type = ArtifactType.SURROGATE
            payload.update(
                {'deployment_params': deployment_params.dict(exclude_unset=True)}
            )

        url = f'/v3/models/{self.model_id}/deploy-surrogate'

        if update:
            http_method = self._client().put
        else:
            http_method = self._client().post

        response = http_method(
            url=url,
            # payload might contain UUID, use custom JSON encoder
            data=payload,
            headers={'Content-Type': 'application/json'},
        )

        job_compact = JobCompactResp(**response.json()['data']['job'])

        logger.info(
            'Model[%s] - Submitted job (%s) for deploying a surrogate model',
            self.model_id,
            job_compact.id,
        )

        return Job.get(id_=job_compact.id)

    @handle_api_error
    def add(
        self,
        dataset_id: UUID | str,
        deployment_params: DeploymentParams | None = None,
    ) -> Job:
        """
        Add a new surrogate.

        :param dataset_id: Dataset to be used for generating surrogate model
        :param deployment_params: Model deployment parameters
        :return: Async job
        """
        job = self._deploy(
            dataset_id=dataset_id, deployment_params=deployment_params, update=False
        )
        return job

    @handle_api_error
    def update(
        self,
        dataset_id: UUID | str,
        deployment_params: DeploymentParams | None = None,
    ) -> Job:
        """
        Update an existing surrogate.

        :param dataset_id: Dataset to be used for generating surrogate model
        :param deployment_params: Model deployment parameters
        :return: Async job
        """
        job = self._deploy(
            dataset_id=dataset_id, deployment_params=deployment_params, update=True
        )
        return job
