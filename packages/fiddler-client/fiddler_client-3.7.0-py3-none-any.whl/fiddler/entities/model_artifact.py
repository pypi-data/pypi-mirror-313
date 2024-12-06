from __future__ import annotations

import os
import logging
import shutil
import tempfile
from pathlib import Path
from typing import Callable
from uuid import UUID

from fiddler.connection import ConnectionMixin
from fiddler.decorators import handle_api_error
from fiddler.entities.file import File
from fiddler.entities.job import Job
from fiddler.schemas.job import JobCompactResp
from fiddler.schemas.model_deployment import DeploymentParams
from fiddler.utils.validations import validate_artifact_dir

logger = logging.getLogger(__name__)


class ModelArtifact(ConnectionMixin):
    def __init__(self, model_id: UUID) -> None:
        """
        Model artifact methods

        :param model_id: Model identifier
        """
        self.model_id = model_id

    def _get_http_method(self, update: bool = False) -> Callable:
        """Get HTTP method based on operation"""
        if update:
            return self._client().put
        return self._client().post

    def _deploy_model_artifact(
        self,
        model_dir: str | Path,
        deployment_params: DeploymentParams | None = None,
        update: bool = False,
    ) -> Job:
        """
        Upload and deploy model artifact for an existing model

        :param model_dir: Model artifact directory
        :param deployment_params: Model deployment parameters
        :param update: Set True for updating artifact, False for adding artifact
        :return: Async job
        """
        model_dir = Path(model_dir)
        validate_artifact_dir(model_dir)

        with tempfile.TemporaryDirectory() as tmp:
            # Archive model artifact directory
            logger.info(
                'Model[%s] - Tarring model artifact directory - %s',
                self.model_id,
                model_dir,
            )
            file_path = shutil.make_archive(
                base_name=str(Path(tmp) / 'files'),
                format='gztar',
                root_dir=str(model_dir),
                base_dir='.',
            )

            logger.info(
                'Model[%s] - Model artifact tar file created at %s - %d bytes',
                self.model_id,
                file_path,
                os.path.getsize(file_path),
            )

            # Upload file
            file = File(path=file_path).upload()

            # Deploy artifact
            assert file.id is not None
            job = self._artifact_deploy(
                file_id=file.id,
                deployment_params=deployment_params,
                update=update,
            )

        logger.info(
            'Model[%s] - Submitted job (%s) for deploying model artifact',
            self.model_id,
            job.id,
        )

        return job

    def _artifact_deploy(
        self,
        file_id: UUID | str,
        deployment_params: DeploymentParams | None = None,
        update: bool = False,
    ) -> Job:
        """Artifact deploy base method."""
        http_method = self._get_http_method(update)
        payload = {
            'file_id': file_id,
            'deployment_params': deployment_params.dict(exclude_unset=True)
            if deployment_params
            else {},
        }

        response = http_method(
            url=f'/v3/models/{self.model_id}/deploy-artifact',
            data=payload,
            headers={'Content-Type': 'application/json'},
        )

        job_compact = JobCompactResp(**response.json()['data']['job'])
        return Job.get(id_=job_compact.id)

    @handle_api_error
    def add(
        self,
        model_dir: str | Path,
        deployment_params: DeploymentParams | None = None,
    ) -> Job:
        """
        Upload and deploy model artifact.

        :param model_dir: Path to model artifact tar file
        :param deployment_params: Model deployment parameters
        :return: Async job instance
        """
        return self._deploy_model_artifact(
            model_dir=model_dir, deployment_params=deployment_params
        )

    @handle_api_error
    def update(
        self,
        model_dir: str | Path,
        deployment_params: DeploymentParams | None = None,
    ) -> Job:
        """
        Update existing model artifact.

        :param model_dir: Path to model artifact tar file
        :param deployment_params: Model deployment parameters
        :return: Async job instance
        """
        return self._deploy_model_artifact(
            model_dir=model_dir, deployment_params=deployment_params, update=True
        )

    @handle_api_error
    def download(
        self,
        output_dir: str | Path,
    ) -> None:
        """
        Download existing model artifact.

        :param output_dir: Path to download model artifact tar file
        """

        output_dir = Path(output_dir)
        if output_dir.exists():
            raise ValueError(f'Output dir already exists {output_dir}')

        with tempfile.TemporaryDirectory() as tmp_dir:
            # Download tar file
            tar_file_path = os.path.join(tmp_dir, 'artifact.tar')

            with self._client().get(
                url=f'/v3/models/{self.model_id}/download-artifact'
            ) as resp:
                resp.raise_for_status()
                with open(tar_file_path, mode='wb') as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            os.makedirs(output_dir, exist_ok=True)
            shutil.unpack_archive(tar_file_path, extract_dir=output_dir, format='tar')
